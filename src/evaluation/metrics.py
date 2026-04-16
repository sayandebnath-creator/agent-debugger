def calculate_score(fix_accuracy, execution_rate, token_efficiency, latency_score):
    # weighted scoring system aligned with README definition
    return int((
        0.4 * fix_accuracy +
        0.2 * execution_rate +
        0.2 * token_efficiency +
        0.2 * latency_score
    ) * 10000)