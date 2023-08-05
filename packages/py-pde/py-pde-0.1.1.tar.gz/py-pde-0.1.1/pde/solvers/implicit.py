"""
Defines an implicit solver
   
.. codeauthor:: David Zwicker <david.zwicker@ds.mpg.de> 
"""

from typing import Callable, Tuple

import numpy as np
import numba as nb

from .base import SolverBase
from ..pdes.base import PDEBase
from ..fields.base import FieldBase
from ..tools.numba import jit



class ConvergenceError(RuntimeError):
    pass



class ImplicitSolver(SolverBase):
    """ class for solving partial differential equations implicitly """

    name = 'implicit'


    def __init__(self, pde: PDEBase,
                 maxiter: int = 100,
                 maxerror: float = 1e-4,
                 backend: str = 'auto'):
        """ initialize the implicit solver
        
        Args:
            pde (:class:`~pde.pdes.base.PDEBase`):
                The instance describing the pde that needs to be solved
            maxiter (int):
                The maximal number of iterations per step
            maxerror (float):
                The maximal error that is permitted in each step
            backend (str):
                Determines how the function is created. Accepted  values are
                'numpy` and 'numba'. Alternatively, 'auto' lets the code decide
                for the most optimal backend.
        """        
        super().__init__(pde)
        self.maxiter = maxiter
        self.maxerror = maxerror
        self.backend = backend
    

    def make_stepper(self, state: FieldBase, dt=None) -> Callable:
        """ return a stepper function using an explicit scheme
        
        Args:
            state (:class:`~pde.fields.FieldBase`):
                An example for the state from which the grid and other
                information can be extracted
            dt (float):
                Time step of the explicit stepping. If `None`, this solver
                specifies 1e-3 as a default value.
                
        Returns:
            Function that can be called to advance the `state` from time
            `t_start` to time `t_end`. The function call signature is
            `(state: numpy.ndarray, t_start: float, t_end: float)`        
        """
        # support `None` as a default value, so the controller can signal that
        # the solver should use a default time step
        if dt is None:
            dt = 1e-3
        
        self.info['dt'] = dt
        self.info['steps'] = 0
        self.info['function_evaluations'] = 0
        self.info['scheme'] = 'implicit-euler'
    
        rhs = self._make_pde_rhs(state, backend=self.backend,
                                 allow_stochastic=False)
        maxiter = int(self.maxiter)
        maxerror2 = self.maxerror ** 2
        
        # handle deterministic  version of the pde
        def inner_stepper(state_data: np.ndarray, t_start: float, steps: int) \
                -> Tuple[float, int]:
            """ compiled inner loop for speed """
            nfev = 0  # count function evaluations
            for i in range(steps):
                t = t_start + i * dt  # current time point
                tn = t + dt           # next time point
                
                # estimate state at next time point 
                evolution_last = dt * rhs(state_data, t)

                for n in range(maxiter):
                    # fixed point iteration for improving state after dt
                    state_guess = state_data + evolution_last
                    evolution_this = dt * rhs(state_guess, tn)
                    
                    # calculate mean squared error
                    err = 0
                    for i in range(state_data.size):
                        err += (state_guess.flat[i] - state_data.flat[i] -
                                evolution_this.flat[i])**2
                    err /= state_data.size
                                
                    if err < maxerror2:
                        # fix point iteration converged
                        break
                    
                    evolution_last = evolution_this
                else:
                    with nb.objmode:
                        self._logger.warn('Implicit Euler step did not '
                                          'converge after %d iterations at '
                                          't=%g (error=%g)', maxiter, t, err)
                    raise ConvergenceError('Implicit Euler step did not '
                                           'converge.')
                nfev += n + 1
                state_data += evolution_this
                     
            return tn, nfev
        
            self.info['stochastic'] = False
            self._logger.info(f'Initialized explicit Euler stepper with dt=%g',
                              dt)
                        
        if self.info['backend'] == 'numba':
            # compile inner step
            inner_stepper = jit(inner_stepper)
        
        def stepper(state: FieldBase, t_start: float, t_end: float) \
                -> float:
            """ use Euler stepping to advance `state` from `t_start` to
            `t_end` """
            # calculate number of steps (which is at least 1)
            steps = max(1, int(np.ceil((t_end - t_start) / dt)))
            t_last, nfev = inner_stepper(state.data, t_start, steps)
            self.info['steps'] += steps
            self.info['function_evaluations'] += nfev
            return t_last        
            
        return stepper

        