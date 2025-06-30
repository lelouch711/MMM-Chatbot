def reallocate_spend(df, allocations):
    """
    Reallocate spend across channels so that new allocations sum to the original total spend.

    Args:
        df: Original DataFrame.
        allocations: dict of {(channel, sub_channel): new_allocation_fraction}
            Example: {('TV', 'National'): 0.5, ('Digital', None): 0.3, ...}
            (values sum to 1.0)
    Returns:
        Updated DataFrame with reallocated spend, sales, and ROI.
    """
    df_result = df.copy()
    total_spend = df['Total Spend (USD)'].sum()

    for (channel, sub_channel), alloc_frac in allocations.items():
        mask = (df_result['Channel'] == channel)
        if pd.notna(sub_channel):
            mask &= (df_result['Sub-Channel'] == sub_channel)
        row_idx = df_result[mask].index

        for idx in row_idx:
            new_spend = total_spend * alloc_frac

            sales_per_dollar = df_result.at[idx, 'Sales Contribution (USD)'] / df_result.at[idx, 'Total Spend (USD)'] if df_result.at[idx, 'Total Spend (USD)'] != 0 else 0
            new_sales = new_spend * sales_per_dollar
            new_roi = new_sales / new_spend if new_spend != 0 else None

            df_result.at[idx, 'Total Spend (USD)'] = new_spend
            df_result.at[idx, 'Sales Contribution (USD)'] = new_sales
            df_result.at[idx, 'ROI'] = new_roi

    return df_result
