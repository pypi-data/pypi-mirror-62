import agros as a2d
from math import pi, sqrt
from tests.scenario import AgrosTestCase
from tests.scenario import AgrosTestResult

class TestGeometry(AgrosTestCase):
    def setUp(self):
        self.problem = a2d.problem(clear = True)
        self.geometry = self.problem.geometry()

    def model(self):
        self.problem = a2d.problem(clear = True)

        self.electrostatic = self.problem.field("electrostatic")
        self.electrostatic.add_boundary("Source", "electrostatic_potential", {"electrostatic_potential" : 10})
        self.electrostatic.add_boundary("Ground", "electrostatic_potential", {"electrostatic_potential" : 0})
        self.electrostatic.add_boundary("Neumann", "electrostatic_surface_charge_density", {"electrostatic_surface_charge_density" : 0})
        self.electrostatic.add_material("Dielectricum", {"electrostatic_permittivity" : 3, "electrostatic_charge_density" : 0})

        self.a = 1.0
        self.b = 1.0

        self.geometry = self.problem.geometry()
        self.geometry.add_edge(0, 0, self.a, 0, boundaries = {"electrostatic" : "Neumann"})
        self.geometry.add_edge(self.a, 0, self.a, self.b, boundaries = {"electrostatic" : "Ground"})
        self.geometry.add_edge(self.a, self.b, 0, self.b, boundaries = {"electrostatic" : "Neumann"})
        self.geometry.add_edge(0, self.b, 0, 0, boundaries = {"electrostatic" : "Source"})
        self.geometry.add_label(self.a/2.0, self.b/2.0, materials = {"electrostatic" : "Dielectricum"})

    """ add_node() """
    def test_add_node(self):
        self.assertEqual(self.geometry.add_node(0, 0), 0)

    def test_add_node_negative_comp(self):
        self.problem.coordinate_type = 'axisymmetric'

        with self.assertRaises(IndexError):
            self.geometry.add_node(-1, 0)

    def test_add_existing_node(self):
        self.geometry.add_node(0, 0)

        with self.assertRaises(RuntimeError):
            self.geometry.add_node(0, 0)

    """ add_edge() """
    def test_add_edge(self):
        self.assertEqual(self.geometry.add_edge(0, 0, 1, 1), 0)

    def test_add_edge_negative_comp(self):
        self.problem.coordinate_type = 'axisymmetric'

        with self.assertRaises(IndexError):
            self.geometry.add_edge(-1, 0, 0, 0)

        with self.assertRaises(IndexError):
            self.geometry.add_edge(0, 0, -1, 0)

    def test_add_edge_with_wrong_angle(self):
        with self.assertRaises(IndexError):
            self.geometry.add_edge(0, 0, 1, 1, angle = -90)

        with self.assertRaises(IndexError):
            self.geometry.add_edge(0, 0, 1, 1, angle = 180)
    
    def test_add_existing_edge(self):
        self.geometry.add_edge(0, 0, 1, 1)

        with self.assertRaises(RuntimeError):
            self.geometry.add_edge(0, 0, 1, 1)

    def test_add_edge_with_boundaries(self):
        with self.assertRaises(ValueError):
            self.geometry.add_edge(0, 0, 1, 1, boundaries = {'wrong_field' : 'wrong_boundary_condition'})

        self.problem.field('electrostatic').add_boundary("Potential", "electrostatic_potential", {"electrostatic_potential" : 1000})
        with self.assertRaises(ValueError):
            self.geometry.add_edge(0, 0, 1, 1, boundaries = {'electrostatic' : 'wrong_boundary_condition'})

        self.assertEqual(self.geometry.add_edge(0, 0, 1, 1, boundaries = {'electrostatic' : 'Potential'}), 0)

    """ add_edge_by_nodes() """
    def test_add_edge_by_nodes(self):
        self.geometry.add_node(0, 0)
        self.geometry.add_node(1, 1)
        self.assertEqual(self.geometry.add_edge_by_nodes(0, 1), 0)

    def test_add_edge_by_same_nodes(self):
        self.geometry.add_node(0, 0)
        with self.assertRaises(RuntimeError):
            self.geometry.add_edge_by_nodes(0, 0)

    def test_add_edge_by_nonexisting_nodes(self):
        self.geometry.add_node(0, 0)
        self.geometry.add_node(1, 1)
        self.geometry.add_edge_by_nodes(0, 1)
        with self.assertRaises(RuntimeError):
            self.geometry.add_edge_by_nodes(0, 1)

    """ modify_edge() """
    def test_modify_edge_angle(self):
        self.model()
        self.geometry.modify_edge(1, angle = 90)
        computation = self.problem.computation()
        computation.solve()
        solution = computation.solution('electrostatic')
        self.assertAlmostEqual(solution.surface_integrals([1])['l'], pi/2.0 * sqrt((self.a/2.0)**2 + (self.b/2.0)**2), 1)

    def test_modify_edge_boundaries(self):
        self.model()
        self.geometry.modify_edge(1, boundaries = {'electrostatic' : 'Ground'})
        computation = self.problem.computation()
        computation.solve()
        solution = computation.solution('electrostatic')
        self.assertAlmostEqual(solution.volume_integrals([0])['We'], 0)

    def test_modify_nonexisting_edge(self):
        self.geometry.add_edge(0, 0, 1, 1)
        with self.assertRaises(IndexError):
            self.geometry.modify_edge(-1, 90)

        with self.assertRaises(IndexError):
            self.geometry.modify_edge(1, 90)

    """ add_label() """
    def test_add_label(self):
        self.assertEqual(self.geometry.add_label(0, 0), 0)

    """ modify_label() """
    def test_modify_label(self):
        pass

class TestGeometryTransformations(AgrosTestCase):
    def model(self):
        self.problem = a2d.problem(clear = True)

        self.electrostatic = self.problem.field("electrostatic")
        self.electrostatic.add_boundary("Source", "electrostatic_potential", {"electrostatic_potential" : 10})
        self.electrostatic.add_boundary("Ground", "electrostatic_potential", {"electrostatic_potential" : 0})
        self.electrostatic.add_boundary("Neumann", "electrostatic_surface_charge_density", {"electrostatic_surface_charge_density" : 0})
        self.electrostatic.add_material("Dielectricum", {"electrostatic_permittivity" : 3, "electrostatic_charge_density" : 0})

        self.a = 1
        self.b = 1

        self.geometry = self.problem.geometry()
        self.geometry.add_edge(0, 0, self.a, 0, boundaries = {"electrostatic" : "Neumann"})
        self.geometry.add_edge(self.a, 0, self.a, self.b, boundaries = {"electrostatic" : "Ground"})
        self.geometry.add_edge(self.a, self.b, 0, self.b, boundaries = {"electrostatic" : "Neumann"})
        self.geometry.add_edge(0, self.b, 0, 0, boundaries = {"electrostatic" : "Source"})
        self.geometry.add_label(self.a/2.0, self.b/2.0, materials = {"electrostatic" : "Dielectricum"})

    def test_move_selection(self):
        pass
        """
        TODO: implement move
        
        self.model()
        dx = 1.5
        dy = 2.5

        self.geometry.select_nodes([1, 2])
        self.geometry.move_selection(dx, 0, False)
        self.geometry.select_edges([2])
        self.geometry.move_selection(0, dy, False)

        computation = self.problem.computation()
        computation.solve()
        solution = computation.solution('electrostatic')
        self.assertAlmostEqual(solution.volume_integrals([0])['V'], (self.a + dx) * (self.b + dy))
        """

    def test_rotate_selection(self):
        pass

    def test_scale_selection(self):
        pass
        """
        TODO: implement move
                
        self.model()
        scale = 2.5

        self.geometry.select_edges(list(range(0, 4)))
        self.geometry.scale_selection(self.a/2.0, self.b/2.0, scale, False)

        computation = self.problem.computation()
        computation.solve()
        solution = computation.solution('electrostatic')
        self.assertAlmostEqual(solution.volume_integrals([0])['S'], (self.a * scale) * (self.b * scale))
        """

if __name__ == '__main__':        
    import unittest as ut
    
    suite = ut.TestSuite()
    result = AgrosTestResult()
    suite.addTest(ut.TestLoader().loadTestsFromTestCase(TestGeometry))
    suite.addTest(ut.TestLoader().loadTestsFromTestCase(TestGeometryTransformations))
    suite.run(result)
