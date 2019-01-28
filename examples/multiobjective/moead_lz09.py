from jmetal.algorithm.multiobjective.moead import MOEAD
from jmetal.operator import PolynomialMutation, DifferentialEvolutionCrossover
from jmetal.problem import LZ09_F2
from jmetal.util.aggregative_function import Chebyshev
from jmetal.util.neighborhood import WeightVectorNeighborhood
from jmetal.util.observer import ProgressBarObserver, VisualizerObserver
from jmetal.util.solution_list import read_solutions, print_function_values_to_file, print_variables_to_file
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.util.visualization import Plot

if __name__ == '__main__':
    problem = LZ09_F2()
    problem.reference_front = read_solutions(filename='../../resources/reference_front/{}.pf'.format(problem.get_name()))

    population_size = 100
    max_evaluations = 175000

    algorithm = MOEAD(
        problem=problem,
        population_size=population_size,
        crossover=DifferentialEvolutionCrossover(CR=1.0, F=0.5, K=0.5),
        mutation=PolynomialMutation(probability=1.0 / problem.number_of_variables, distribution_index=20),
        aggregative_function=Chebyshev(dimension=problem.number_of_objectives),
        neighbourhood=WeightVectorNeighborhood(population_size, 20, weights_path='../../resources/MOEAD_weights/'),
        neighbourhood_selection_probability=0.9,
        max_number_of_replaced_solutions=2,
        termination_criterion=StoppingByEvaluations(max=max_evaluations)
    )

    progress_bar = ProgressBarObserver(max=max_evaluations)
    algorithm.observable.register(observer=progress_bar)
    algorithm.observable.register(observer=VisualizerObserver(reference_front=problem.reference_front, display_frequency=500))

    algorithm.run()
    front = algorithm.get_result()

    label = algorithm.get_name() + "." + problem.get_name()
    algorithm_name = label
    # Plot front
    plot_front = Plot(plot_title='Pareto front approximation', axis_labels=problem.obj_labels)
    plot_front.plot(front, label=label, filename=algorithm_name)

    # Plot interactive front
    plot_front = InteractivePlot(plot_title='Pareto front approximation', axis_labels=problem.obj_labels)
    plot_front.plot(front, label=label, filename=algorithm_name)

    # Save results to file
    print_function_values_to_file(front, 'FUN.' + label)
    print_variables_to_file(front, 'VAR.'+ label)


    print('Algorithm (continuous problem): ' + algorithm.get_name())
    print('Problem: ' + problem.get_name())
    print('Computing time: ' + str(algorithm.total_computing_time))
