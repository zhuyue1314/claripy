import claripy
import nose

def test_simple_merging():
    raw_simple_merging(claripy.solvers.BranchingSolver)
    raw_simple_merging(claripy.solvers.CompositeSolver)

def raw_simple_merging(solver_type):
    clrp = claripy.Claripies["SerialZ3"]
    s1 = solver_type(clrp)
    s2 = solver_type(clrp)
    w = clrp.BitVec("w", 8)
    x = clrp.BitVec("x", 8)
    y = clrp.BitVec("y", 8)
    z = clrp.BitVec("z", 8)
    m = clrp.BitVec("m", 8)

    s1.add([x == 1, y == 10])
    s2.add([x == 2, z == 20, w == 5])
    _, sm = s1.merge([s2], m, [ 0, 1 ])

    nose.tools.assert_equal(s1.eval(x, 1), (1,))
    nose.tools.assert_equal(s2.eval(x, 1), (2,))

    sm1 = sm.branch()
    sm1.add(x == 1)
    nose.tools.assert_equal(sm1.eval(x, 1), (1,))
    nose.tools.assert_equal(sm1.eval(y, 1), (10,))
    nose.tools.assert_equal(sm1.eval(z, 1), (0,))
    nose.tools.assert_equal(sm1.eval(w, 1), (0,))

    sm2 = sm.branch()
    sm2.add(x == 2)
    nose.tools.assert_equal(sm2.eval(x, 1), (2,))
    nose.tools.assert_equal(sm2.eval(y, 1), (0,))
    nose.tools.assert_equal(sm2.eval(z, 1), (20,))
    nose.tools.assert_equal(sm2.eval(w, 1), (5,))

    sm1 = sm.branch()
    sm1.add(m == 0)
    nose.tools.assert_equal(sm1.eval(x, 1), (1,))
    nose.tools.assert_equal(sm1.eval(y, 1), (10,))
    nose.tools.assert_equal(sm1.eval(z, 1), (0,))
    nose.tools.assert_equal(sm1.eval(w, 1), (0,))

    sm2 = sm.branch()
    sm2.add(m == 1)
    nose.tools.assert_equal(sm2.eval(x, 1), (2,))
    nose.tools.assert_equal(sm2.eval(y, 1), (0,))
    nose.tools.assert_equal(sm2.eval(z, 1), (20,))
    nose.tools.assert_equal(sm2.eval(w, 1), (5,))

    m2 = clrp.BitVec("m2", 32)
    _, smm = sm1.merge([sm2], m2, [0, 1])

    smm_1 = smm.branch()
    smm_1.add(x == 1)
    nose.tools.assert_equal(smm_1.eval(x, 1), (1,))
    nose.tools.assert_equal(smm_1.eval(y, 1), (10,))
    nose.tools.assert_equal(smm_1.eval(z, 1), (0,))
    nose.tools.assert_equal(smm_1.eval(w, 1), (0,))

    smm_2 = smm.branch()
    smm_2.add(m == 1)
    nose.tools.assert_equal(smm_2.eval(x, 1), (2,))
    nose.tools.assert_equal(smm_2.eval(y, 1), (0,))
    nose.tools.assert_equal(smm_2.eval(z, 1), (20,))
    nose.tools.assert_equal(smm_2.eval(w, 1), (5,))

    so = solver_type(clrp)
    so.add(w == 0)

    sa = so.branch()
    sb = so.branch()
    sa.add(x == 1)
    sb.add(x == 2)
    _, sm = sa.merge([sb], m, [0, 1])

    smc = sm.branch()
    smd = sm.branch()
    smc.add(y == 3)
    smd.add(y == 4)

    _, smm = smc.merge([smd], m2, [0, 1])
    wxy = clrp.Concat(w, x, y)

    smm_1 = smm.branch()
    smm_1.add(wxy == 0x000103)
    nose.tools.assert_true(smm_1.satisfiable())

    smm_1 = smm.branch()
    smm_1.add(wxy == 0x000104)
    nose.tools.assert_true(smm_1.satisfiable())

    smm_1 = smm.branch()
    smm_1.add(wxy == 0x000203)
    nose.tools.assert_true(smm_1.satisfiable())

    smm_1 = smm.branch()
    smm_1.add(wxy == 0x000204)
    nose.tools.assert_true(smm_1.satisfiable())

    smm_1 = smm.branch()
    smm_1.add(wxy != 0x000103)
    smm_1.add(wxy != 0x000104)
    smm_1.add(wxy != 0x000203)
    smm_1.add(wxy != 0x000204)
    nose.tools.assert_false(smm_1.satisfiable())

if __name__ == '__main__':
    test_simple_merging()