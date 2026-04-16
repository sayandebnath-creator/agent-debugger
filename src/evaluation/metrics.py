def calculate_score(fix_accuracy, execution_rate, token_efficiency, latency_score):
    """
    All inputs normalized between 0 and 1
    """
    final_score = (
        0.4 * fix_accuracy +
        0.2 * execution_rate +
        0.2 * token_efficiency +
        0.2 * latency_score
    )
    return int(final_score * 10000)