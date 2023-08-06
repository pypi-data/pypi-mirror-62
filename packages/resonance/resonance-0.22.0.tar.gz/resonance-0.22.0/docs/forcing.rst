Single Degree of Freedom Nonlinear System


.. jupyter-execute::

   from resonance.linear_systems import SingleDoFLinearSystem

   msd_sys = SingleDoFLinearSystem()

.. jupyter-execute::

   msd_sys.constants['m'] = 1.0  # kg
   msd_sys.constants['fn'] = 1.0  # Hz
   msd_sys.constants['zeta'] = 0.1  # unitless

   msd_sys.constants

Define the coordinate and speed. The software assumes that the speed is defined
as the time derivative of the coordinate, i.e. :math:`v = \dot{x}`.

.. jupyter-execute::

   msd_sys.coordinates['x'] = 1.0  # m
   msd_sys.speeds['v'] = 0.0  # m/s

.. jupyter-execute::

   msd_sys.coordinates

.. jupyter-execute::

   msd_sys.speeds

.. jupyter-execute::

   msd_sys.states

.. jupyter-execute::

    def calc_step_input(Fo, omega, time):
        if time < 1.0:
         return Fo
        else:
         return 0.0
        return Fo*np.cos(omega_time)

    msd.add_forcing('F', calc_input)
    msd.forcing

.. jupyter-execute::

   def eval_eom(x, v, m, fn, zeta, F):

       wn = 2*np.pi*fn
       k = m*wn**2
       c = zeta*2*wn*m

       xdot = v
       vdot = F/m - c/m*v - k/m*x

       return xdot, vdot

    msd.diff_eq_func = eval_eom


