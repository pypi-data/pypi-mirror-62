Command Line Scripts
====================

When installing NegMAS through the pip command, you get one command line tool that can be used to
aid your development and testing. This tool provides a unified interface to all negmas commands.

The set of supported commands are:

===============       ===================================================================
 Command                                  Meaning
===============       ===================================================================
tournament            Manages a tournament (create, run, evaluate)
run2019               Runs a 2019 tournament
run2020               Runs a 2020 tournament
version               Prints SCML version (and NegMAS version)
===============       ===================================================================

Tournament Command (scml tournament)
--------------------------------------

The Tournament command (`tournament` ) allows you to run a tournament between different agents in some world and
compare their relative performance. The tool is general enough to support several world types.


You can get help on this tool by running:

.. code-block:: console

    $ negmas tournament --help

The `tournament` command has a set of sub-commands for creating, running, and combining tournament results as follows:

========  ================================================
Command   Action
========  ================================================
 combine  Finds winners of an arbitrary set of tournaments
 create   Creates a tournament
 run      Runs/continues a tournament
 winners  Finds winners of a tournament or a set of
          tournaments sharing
========  ================================================


Creating a tournament
~~~~~~~~~~~~~~~~~~~~~

These are the *optional* arguments of this tool:

========================================== ==============================================================
  Argument                                      Meaning
========================================== ==============================================================
  -n, --name TEXT                           The name of the tournament. The special
                                            value "random" will result in a random name
                                            [default: random]
  -s, --steps INTEGER                       Number of steps. If passed then --steps-min
                                            and --steps-max are ignored
  --steps-min INTEGER                       Minimum number of steps (only used if
                                            --steps was not passed  [default: 50]
  --steps-max INTEGER                       Maximum number of steps (only used if
                                            --steps was not passed  [default: 100]
  -t, --timeout INTEGER                     Timeout the whole tournament after the given
                                            number of seconds (0 for infinite)
                                            [default: 0]
  --configs INTEGER                         Number of unique configurations to generate.
                                            [default: 5]
  --runs INTEGER                            Number of runs for each configuration
                                            [default: 2]
  --max-runs INTEGER                        Maximum total number of runs. Zero or
                                            negative numbers mean no limit  [default: -1]
  --agents INTEGER                          Number of agents per competitor (not used
                                            for *std in which this is preset to
                                            1).  [default: 3]
  --factories INTEGER                       Minimum numbers of factories to have per
                                            level.  [default: 5]
  --competitors TEXT                        A semicolon (;) separated list of agent
                                            types to use for the competition.
  --jcompetitors, --java-competitors TEXT   A semicolon (;) separated list of agent
                                            types to use for the competition.
  --non-competitors TEXT                    A semicolon (;) separated list of agent
                                            types to exist in the worlds as non-
                                            competitors (their scores will not be
                                            calculated).
  -l, --log DIRECTORY                       Default location to save logs (A folder will
                                            be created under it)  [default:
                                            ~/negmas/logs/tournaments]
  --world-config FILE                       A file to load extra configuration
                                            parameters for world simulations from.
  --verbosity INTEGER                       verbosity level (from 0 == silent to 1 ==
                                            world progress)  [default: 1]
  --reveal-names / --hidden-names           Reveal agent names (should be used only for
                                            debugging)  [default: True]
  --log-ufuns / --no-ufun-logs              Log ufuns into their own CSV file. Only
                                            effective if --debug is given  [default: False]
  --log-negs / --no-neg-logs                Log all negotiations. Only effective if
                                            --debug is given  [default: False]
  --compact / --debug                       If True, effort is exerted to reduce the
                                            memory footprint whichincludes reducing logs
                                            dramatically.  [default: True]
  --raise-exceptions / --ignore-exceptions  Whether to ignore agent exceptions [default: True]
  --path TEXT                               A path to be added to PYTHONPATH in which
                                            all competitors are stored. You can path a :
                                            separated list of paths on linux/mac and a ;
                                            separated list in windows
  --ttype TEXT                              The tournament type. Supported types are scml2019std
                                            , scml2019collusion, scml2019sabotage, scml2020std
                                            , scml2020collusion.  You can also use anac* instead
                                            of scml*. [default: scml2020collusion]
  --cw INTEGER                              Number of competitors to run at every world
                                            simulation. It must either be left at
                                            default or be a number > 1 and < the number
                                            of competitors passed using --competitors
  --config FILE                             Read configuration from FILE.
========================================== ==============================================================


Running a tournament
~~~~~~~~~~~~~~~~~~~~

After creating a tournament using the `tournament create` command, it can be run using the `tournament run` command.
The parameters for this command are:

========================================== ==============================================================
 Argument                                   Meaning
========================================== ==============================================================
  -n, --name TEXT                           The name of the tournament. When invoked
                                            after create, there is no need to pass it
  -l, --log DIRECTORY                       Default location to save logs  [default:
                                            ~/negmas/logs/tournaments]
  --verbosity INTEGER                       verbosity level (from 0 == silent to 1 ==
                                            world progress)  [default: 1]
  --parallel / --serial                     Run a parallel/serial tournament on a single
                                            machine  [default: True]
  --distributed /  --single-machine         Run a distributed tournament using dask
                                            [default: False]
  --ip TEXT                                 The IP address for a dask scheduler to run
                                            the distributed tournament. Effective only
                                            if --distributed  [default: 127.0.0.1]
  --port INTEGER                            The IP port number a dask scheduler to run
                                            the distributed tournament. Effective only
                                            if --distributed  [default: 8786]
  --compact / --debug                       If True, effort is exerted to reduce the
                                            memory footprint whichincludes reducing logs
                                            dramatically.  [default: True]
  --path TEXT                               A path to be added to PYTHONPATH in which
                                            all competitors are stored. You can path a :
                                            separated list of paths on linux/mac and a ;
                                            separated list in windows
  --metric TEXT                             The statistical metric used for choosing the
                                            winners. Possibilities are mean, median,
                                            std, var, sum  [default: mean]
  --config FILE                             Read configuration from FILE.
========================================== ==============================================================


Upon completion, a complete log and several statistics are saved in a new folder under the `log folder` location
specified by the `--log` argument (default is negmas/logs/tournaments under the HOME directory). To avoid over-writing
earlier results, a new folder will be created for each run named by the current date and time. The
folder will contain the following files:


=========================   ========     =================================================================
 File/Folder Name             Format         Content
=========================   ========     =================================================================
configs                     FOLDER       Contains one json file for each world
                                         run tried during the tournament. You can
                                         re-run this world using `run_world` function in the `tournament`
                                         module.
params.json                 JSON         The parameters used to create this tournament
base_configs.json           JSON         The base configurations used in the tournament (without agent/factory
                                         assignments.
assigned_configs.json       JSON         The configurations used after assigning factories to managers
scores.csv                  CSV          Scores of every agent in every world
total_scores.csv            CSV          Scores of every agent **type** averaged over all runs
winners.csv                 CSV          Winner *types* and their average scores
ttest.csv                   CSV          Results of a factorial TTEST comparing the performance of all
                                         agent *types*
=========================   ========     =================================================================

Other than these files, a folder with the same number as the corresponding config file in the configs folder, keeps full
statistics/log of every world *but only if --debug is specified* (see the `SCML2020World Runner` section for the contents of
this folder.

Combining tournament results
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Can be used to combine the results of multiple tournaments runs using tournament `combine`.
The parameters of this command are:

======================  =======================================================
 Argument                 Meaning
======================  =======================================================
  -d, --dest DIRECTORY  The location to save the results
  --metric TEXT         The statistical metric used for choosing the winners.
                        Possibilities are mean, median, std, var, sum
                        [default: median]
  --config FILE         Read configuration from FILE.
======================  =======================================================


Finding the winners of a tournament
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To report the winners of a tournament, you can use tournament `winners` . The parameters of this command are:

============================== =======================================================
 Argument                       Meaning
============================== =======================================================
  -n, --name TEXT               The name of the tournament. When invoked after
                                create, there is no need to pass it
  -l, --log DIRECTORY           Default location to save logs  [default:
                                ~/negmas/logs/tournaments]
  --recursive / --no-recursive  Whether to recursively look for tournament
                                results. --name should not be given if
                                --recursive  [default: True]
  --metric TEXT                 The statistical metric used for choosing the
                                winners. Possibilities are mean, median, std,
                                var, sum  [default: median]
  --config FILE                 Read configuration from FILE.
============================== =======================================================

Running an SCML2020 world (scml run2020)
----------------------------------------

Runs a single world simulation of SCML2020.

================================================ =======================================================
  Parameter                                         Meaning
================================================ =======================================================
  --steps INTEGER                                 Number of steps.  [default: 10]
  --processes INTEGER                             Number of processes. Should never be less
                                                  than 2  [default: 3]
  --neg-speedup INTEGER                           Negotiation Speedup.  [default: 21]
  --agents INTEGER                                Number of agents (miners/negmas.consumers)
                                                  per production level  [default: 5]
  --horizon INTEGER                               Exogenous contracts horizon.  [default: 15]
  --time INTEGER                                  Total time limit.  [default: 7200]
  --neg-time INTEGER                              Time limit per single negotiation  [default: 120]
  --neg-steps INTEGER                             Number of rounds per single negotiation [default: 20]
  --lines INTEGER                                 The number of lines per factory  [default: 10]
  --competitors TEXT                              A semicolon (;) separated list of agent
                                                  types to use for the competition.  [default: RandomAgent]
  --log DIRECTORY                                 Default location to save logs (A folder will
                                                  be created under it)  [default: ~/negmas/logs]
  --log-ufuns / --no-ufun-logs                    Log ufuns into their own CSV file. Only
                                                  effective if --debug is given  [default: False]
  --log-negs / --no-neg-logs                      Log all negotiations. Only effective if
                                                  --debug is given  [default: False]
  --compact / --debug                             If True, effort is exerted to reduce the
                                                  memory footprint whichincludes reducing logs
                                                  dramatically.  [default: False]
  --raise-exceptions / --ignore-exceptions        Whether to ignore agent exceptions [default: True]
  --balance INTEGER                               Initial balance of all factories. A negative
                                                  number will make the balance automatically
                                                  calculated by the system. It will go up with
                                                  process level  [default: -1]
  --path TEXT                                     A path to be added to PYTHONPATH in which
                                                  all competitors are stored. You can path a :
                                                  separated list of paths on linux/mac and a ;
                                                  separated list in windows  [default: ]
  --world-config FILE                             A file to load extra configuration
                                                  parameters for world simulations from.
  --config FILE                                   Read configuration from FILE.
  --help                                          Show this message and exit.
================================================ =======================================================


Running an SCML2019 world (scml run2019)
----------------------------------------

Runs a single world simulation of SCML2019.

================================================ =======================================================
  Parameter                                         Meaning
================================================ =======================================================
  --steps INTEGER                                 Number of steps.  [default: 10]
  --levels INTEGER                                Number of intermediate production levels
                                                  (processes). -1 means a single product and
                                                  no factories.  [default: 3]
  --neg-speedup INTEGER                           Negotiation Speedup.  [default: 21]
  --agents INTEGER                                Number of agents (miners/negmas.consumers)
                                                  per production level  [default: 5]
  --horizon INTEGER                               Exogenous contracts horizon.  [default: 15]
  --time INTEGER                                  Total time limit.  [default: 7200]
  --neg-time INTEGER                              Time limit per single negotiation  [default: 120]
  --neg-steps INTEGER                             Number of rounds per single negotiation [default: 20]
  --lines INTEGER                                 The number of lines per factory  [default: 10]
  --competitors TEXT                              A semicolon (;) separated list of agent
                                                  types to use for the competition.
                                                  [default: GreedyFactoryManager]
  --log DIRECTORY                                 Default location to save logs (A folder will
                                                  be created under it)  [default: ~/negmas/logs]
  --log-ufuns / --no-ufun-logs                    Log ufuns into their own CSV file. Only
                                                  effective if --debug is given  [default: False]
  --log-negs / --no-neg-logs                      Log all negotiations. Only effective if
                                                  --debug is given  [default: False]
  --compact / --debug                             If True, effort is exerted to reduce the
                                                  memory footprint whichincludes reducing logs
                                                  dramatically.  [default: False]
  --raise-exceptions / --ignore-exceptions        Whether to ignore agent exceptions [default: True]
  --balance INTEGER                               Initial balance of all factories. A negative
                                                  number will make the balance automatically
                                                  calculated by the system. It will go up with
                                                  process level  [default: -1]
  --min-consumption INTEGER                       The minimum number of units consumed by each
                                                  consumer at every time-step.  [default: 3]
  --max-consumption INTEGER                       The maximum number of units consumed by each
                                                  consumer at every time-step.  [default: 5]
  --horizon INTEGER                               Consumption horizon.  [default: 15]
  --transport INTEGER                             Transportation Delay.  [default: 0]
  --sign INTEGER                                  The default delay between contract
                                                  conclusion and signing  [default: 1]
  --guaranteed TEXT                               Whether to only sign contracts that are
                                                  guaranteed not to cause breaches  [default:
                                                  False]
  --retrials INTEGER                              The number of times an agent re-tries on
                                                  failed negotiations  [default: 2]
  --use-consumer / --no-consumer                  Use internal consumer object in factory
                                                  managers  [default: True]
  --max-insurance FLOAT                           Use insurance against partner in factory
                                                  managers up to this premium. Pass zero for
                                                  never buying insurance and a 'inf' (without
                                                  quotes) for infinity.  [default: inf]
  --riskiness FLOAT                               How risky is the default factory manager
                                                  [default: 0.0]
  --shared-profile / --multi-profile              If True, all lines in the same factory will
                                                  have the same cost.  [default: True]
  --reserved-value FLOAT                          The reserved value used by
                                                  GreedyFactoryManager  [default: -inf]
  --path TEXT                                     A path to be added to PYTHONPATH in which
                                                  all competitors are stored. You can path a :
                                                  separated list of paths on linux/mac and a ;
                                                  separated list in windows  [default: ]
  --world-config FILE                             A file to load extra configuration
                                                  parameters for world simulations from.
  --config FILE                                   Read configuration from FILE.
  --help                                          Show this message and exit.
================================================ =======================================================
