# ActivitySim
# See full license in LICENSE.txt.

import os
import logging

import numpy as np
import pandas as pd

from activitysim.core import simulate as asim
from activitysim.core import tracing
from activitysim.core import config


logger = logging.getLogger(__name__)


def compute_logsums(choosers, logsum_spec, logsum_settings,
                    skim_dict, skim_stack, alt_col_name,
                    chunk_size, trace_hh_id):

    trace_label = trace_hh_id and 'compute_logsums'

    nest_spec = config.get_logit_model_settings(logsum_settings)
    constants = config.get_model_constants(logsum_settings)

    logger.info("Running compute_logsums with %d choosers" % len(choosers.index))

    if trace_hh_id:
        tracing.trace_df(logsum_spec,
                         tracing.extend_trace_label(trace_label, 'spec'),
                         slicer='NONE', transpose=False)

    # setup skim keys
    odt_skim_stack_wrapper = skim_stack.wrap(left_key='TAZ', right_key=alt_col_name,
                                             skim_key="out_period")
    dot_skim_stack_wrapper = skim_stack.wrap(left_key=alt_col_name, right_key='TAZ',
                                             skim_key="in_period")
    od_skim_stack_wrapper = skim_dict.wrap('TAZ', alt_col_name)

    skims = [odt_skim_stack_wrapper, dot_skim_stack_wrapper, od_skim_stack_wrapper]

    locals_d = {
        "odt_skims": odt_skim_stack_wrapper,
        "dot_skims": dot_skim_stack_wrapper,
        "od_skims": od_skim_stack_wrapper
    }
    if constants is not None:
        locals_d.update(constants)

    logsums = asim.simple_simulate_logsums(
        choosers,
        logsum_spec,
        nest_spec,
        skims=skims,
        locals_d=locals_d,
        chunk_size=chunk_size,
        trace_label=trace_label)

    return logsums
