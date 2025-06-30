def increase_total_spend(df,changes):
    df_results = df.copy()
    results = []

    for(channel,sub_channel), pct_change in changes.items():
        mask = (df_results["Channel"] == channel)
        if pd.notna(sub_channel):
            mask &= (df_results['Sub_Channel']  == sub_channel)
        row_idx = df_results[mask].index

        for idx in row_idx:
            orig_spend = df_results.at[idx,'Total Spend (USD)']
            orig_sales = df_results.at[idx,'Sales Contribution (USD)']
            orig_roi = df_results.at[idx,'ROI']


            #Linear Scaling
            new_spend = orig_spend * (1 + pct_change / 100)
            new_sales = orig_sales * (1 + pct_change / 100)
            new_roi = new_sales / new_spend if new_spend != 0 else None

            # Update in the copied dataframe
            df_results.at[idx, 'Total Spend (USD)'] = new_spend
            df_results.at[idx, 'Sales Contribution (USD)'] = new_sales
            df_results.at[idx, 'ROI'] = new_roi

            results.append({
                "Channel": channel,
                "Sub-Channel": sub_channel,
                "Original Spend": orig_spend,
                "New Spend": new_spend,
                "Original Sales": orig_sales,
                "New Sales": new_sales,
                "Original ROI": orig_roi,
                "New ROI": new_roi,
                "Spend Change (%)": pct_change
            })
    # Return summary DataFrame of changes
    return pd.DataFrame(results), df_results
