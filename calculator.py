def calculate_equity_intraday(buy_price, sell_price, quantity, exchange='NSE'):
    # Turnover
    turnover = (buy_price + sell_price) * quantity

    # Brokerage
    brokerage_buy = min(0.0003 * buy_price * quantity, 20)
    brokerage_sell = min(0.0003 * sell_price * quantity, 20)
    brokerage = brokerage_buy + brokerage_sell

    # STT on sell side only, 0.025%
    stt = 0.00025 * sell_price * quantity

    # Exchange Transaction Charges
    etc_rate = 0.0000345  # 0.00345%
    etc = etc_rate * turnover

    # SEBI Charges
    sebi_charges = 0.000001 * turnover

    # GST
    gst = 0.18 * (brokerage + etc)

    # Stamp Duty on buy side only
    stamp_duty = 0.00003 * buy_price * quantity

    # Total Charges
    total_charges = brokerage + stt + etc + gst + sebi_charges + stamp_duty

    # Gross Profit
    gross_profit = (sell_price - buy_price) * quantity

    # Net P&L
    net_pnl = gross_profit - total_charges

    # Points to breakeven
    points_to_breakeven = total_charges / quantity

    result = {
        'turnover': turnover,
        'brokerage': brokerage,
        'stt': stt,
        'exchange_txn_charges': etc,
        'sebi_charges': sebi_charges,
        'gst': gst,
        'stamp_duty': stamp_duty,
        'total_charges': total_charges,
        'gross_profit': gross_profit,
        'net_profit': net_pnl,
        'points_to_breakeven': points_to_breakeven,
    }

    return result

print("Equity Intraday Calculation:")
buy_price = 1000  # Buy price per share
sell_price = 1100  # Sell price per share
quantity = 400  # Number of shares
exchange = 'NSE'  # Exchange: 'NSE' or 'BSE'

result_intraday = calculate_equity_intraday(buy_price, sell_price, quantity, exchange)

print(f"Net Profit: {result_intraday['net_profit']}")
print(f"Total Charges: {result_intraday['total_charges']}")
print(f"Points to Break-even: {result_intraday['points_to_breakeven']}\n")
