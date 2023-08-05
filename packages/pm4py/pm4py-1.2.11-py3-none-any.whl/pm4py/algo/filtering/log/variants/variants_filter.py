from pm4py.statistics.variants.log.get import get_variants_from_log_trace_idx, get_variants, get_variants_along_with_case_durations, get_variants_sorted_by_count, convert_variants_trace_idx_to_trace_obj
from pm4py.algo.filtering.common import filtering_constants
from pm4py.objects.log.log import EventLog
from pm4py.util.xes_constants import DEFAULT_NAME_KEY
from pm4py.util.constants import PARAMETER_CONSTANT_ACTIVITY_KEY


def apply(log, admitted_variants, parameters=None):
    """
    Filter log keeping/removing only provided variants

    Parameters
    -----------
    log
        Log object
    admitted_variants
        Admitted variants
    parameters
        Parameters of the algorithm, including:
            activity_key -> Attribute identifying the activity in the log
            positive -> Indicate if events should be kept/removed
    """

    if parameters is None:
        parameters = {}
    positive = parameters["positive"] if "positive" in parameters else True
    variants = get_variants(log, parameters=parameters)
    log = EventLog()
    for variant in variants:
        if (positive and variant in admitted_variants) or (not positive and variant not in admitted_variants):
            for trace in variants[variant]:
                log.append(trace)
    return log


def filter_by_variants_percentage(log, percentage=0.8, parameters=None):
    """
    Filters a log by variants percentage

    Parameters
    -------------
    log
        Event log
    percentage
        Percentage
    parameters
        Parameters of the algorithm

    Returns
    -------------
    filtered_log
        Filtered log (by variants percentage)
    """
    if parameters is None:
        parameters = {}

    variants = get_variants(log, parameters=parameters)
    var_with_count = sorted([(x, len(y)) for x, y in variants.items()])

    total_sum = sum(x[1] for x in var_with_count)
    partial_sum = 0

    variants_to_filter = []

    for i in range(len(var_with_count)):
        partial_sum = partial_sum + var_with_count[i][1]
        variants_to_filter.append(var_with_count[i][0])

        if partial_sum >= total_sum * percentage and (i == len(var_with_count)-1 or (i < len(var_with_count)-1 and var_with_count[i+1][1] < var_with_count[i][1])):
            break

    return apply(log, variants_to_filter, parameters=parameters)


def filter_log_by_variants_percentage(log, variants, variants_percentage=0.0):
    """
    Filter the log by variants percentage

    Parameters
    ----------
    log
        Log
    variants
        Dictionary with variant as the key and the list of traces as the value
    variants_percentage
        Percentage of variants that should be kept (the most common variant is always kept)

    Returns
    ----------
    filtered_log
        Filtered log
    """
    filtered_log = EventLog()
    no_of_traces = len(log)
    variant_count = get_variants_sorted_by_count(variants)
    already_added_sum = 0

    for i in range(len(variant_count)):
        variant = variant_count[i][0]
        varcount = variant_count[i][1]
        percentage_already_added = already_added_sum / no_of_traces
        if already_added_sum == 0 or percentage_already_added < variants_percentage:
            for trace in variants[variant]:
                filtered_log.append(trace)
            already_added_sum = already_added_sum + varcount

    return filtered_log


def find_auto_threshold(log, variants, decreasing_factor):
    """
    Find automatically variants filtering threshold
    based on specified decreasing factor
    
    Parameters
    ----------
    log
        Log
    variants
        Dictionary with variant as the key and the list of traces as the value
    decreasing_factor
        Decreasing factor (stops the algorithm when the next variant by occurrence is below this factor
        in comparison to previous)
    
    Returns
    ----------
    variantsPercentage
        Percentage of variants to keep in the log
    """
    no_of_traces = len(log)
    variant_count = get_variants_sorted_by_count(variants)
    already_added_sum = 0

    prev_var_count = -1
    percentage_already_added = 0
    for i in range(len(variant_count)):
        varcount = variant_count[i][1]
        percentage_already_added = already_added_sum / no_of_traces
        if already_added_sum == 0 or varcount > decreasing_factor * prev_var_count:
            already_added_sum = already_added_sum + varcount
        else:
            break
        prev_var_count = varcount

    percentage_already_added = already_added_sum / no_of_traces

    return percentage_already_added


def apply_auto_filter(log, variants=None, parameters=None):
    """
    Apply a variants filter detecting automatically a percentage
    
    Parameters
    ----------
    log
        Log
    variants
        Variants contained in the log
    parameters
        Parameters of the algorithm, including:
            activity_key -> Key that identifies the activity
            decreasingFactor -> Decreasing factor (stops the algorithm when the next variant by occurrence is below
            this factor in comparison to previous)
    
    Returns
    ----------
    filteredLog
        Filtered log
    """
    if parameters is None:
        parameters = {}

    attribute_key = parameters[
        PARAMETER_CONSTANT_ACTIVITY_KEY] if PARAMETER_CONSTANT_ACTIVITY_KEY in parameters else DEFAULT_NAME_KEY
    decreasing_factor = parameters[
        "decreasingFactor"] if "decreasingFactor" in parameters else filtering_constants.DECREASING_FACTOR

    parameters_variants = {PARAMETER_CONSTANT_ACTIVITY_KEY: attribute_key}
    if variants is None:
        variants = get_variants(log, parameters=parameters_variants)
    variants_percentage = find_auto_threshold(log, variants, decreasing_factor)
    filtered_log = filter_log_by_variants_percentage(log, variants, variants_percentage)
    return filtered_log
