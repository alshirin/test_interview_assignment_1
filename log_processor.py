import re
import pandas as pd
from typing import Iterable

LOG_FILE = "qa_ExpTester_PreInterview_Assigment.log"
PATH = "./"

PATTERNS = {
    "client_ip": r"\[FROM\]: \[(.*?)\]",
    "request_symbol": r"symbol:(\d+)",
    "request_side": r"side:(\w+)",
    "request_quantity": r"quantity:([\d.]+)",
    "request_signature": r"signature:([\w]+)",
    "request_price": r"price:([\d.]+)",
    "request_type": r"type:(\w+)",
    "request_timeInForce": r"timeInForce:(\w+)",
    "request_recvWindow": r"recvWindow:(\d+)",
    "request_timestamp": r"timestamp:(\d+)",
    "acct": r"\[ACCT\]: ([\d|]+)",
    "response": r"\[RESP\]: ([\d/]+)",
    "proc": r"proc:([\d.]+)ms",
    "proxy": r"proxy:([-]?\d+)ms",
    "session": r"session:([-]?\d+)ms",
    "http_status": r"httpStatus:(\d+)",
    "response_code": r'"code":(-\d+)',
    "response_msg": r'"msg":"([^"]+)"',
    "response_symbol": r'"symbol":"(\w+)"',
    "response_orderId": r'"orderId":(\d+)',
    "response_clientOrderId": r'"clientOrderId":"(\w+)"',
    "response_transactTime": r'"transactTime":(\d+)',
    "response_price": r'"price":"([\d.]+)"',
    "response_origQty": r'"origQty":"([\d.]+)"',
    "response_executedQty": r'"executedQty":"([\d.]+)"',
    "calculated_LeavesQty": r'"calculated_LeavesQty":"^a{0}$"',
    "response_cummulativeQuoteQty": r'"cummulativeQuoteQty":"([\d.]+)"',
    "response_status": r'"status":"(\w+)"',
    "response_timeInForce": r'"timeInForce":"(\w+)"',
    "response_type": r'"type":"(\w+)"',
    "response_side": r'"side":"(\w+)"',
    "response_fills": r'"fills":(\[.*?\])',
}


def read_log_file_generator(file_path: str) -> Iterable:
    with open(file_path, "r", encoding="utf-8", errors="replace") as file:
        for line in file:
            yield line


def convert_api_requests_to_dataframe(log_reader: Iterable) -> pd.DataFrame:
    def calculate_leaves_quantity(req: dict) -> float | int | None:
        if req["response_fills"]:
            leaves_quantity = float(req.get("response_origQty", 0)) - float(
                req.get("response_executedQty", 0)
            )
            return leaves_quantity
        return req["response_origQty"]

    api_requests = []
    for log_line in log_reader:
        if "/api/v3/order" in log_line:
            api_request = {
                key: re.search(value, log_line) for key, value in PATTERNS.items()
            }
            request = {
                key: value.group(1) if value else None
                for key, value in api_request.items()
            }

            request["calculated_LeavesQty"] = calculate_leaves_quantity(request)

            api_requests.append(request)
    return pd.DataFrame(api_requests)


def show_orders_per_second_stat(dataframe: pd.DataFrame) -> None:
    dataframe["request_timestamp_sec"] = (
        dataframe["request_timestamp"].astype(int) // 1000
    )

    df = (
        dataframe.groupby("request_timestamp_sec")
        .size()
        .reset_index(name="requests_per_second")
    )
    print("MAX Requests Per Second value:", df["requests_per_second"].max())
    print("MIN Requests Per Second value:", df["requests_per_second"].min())
    print("AVG Requests Per Second value:", df["requests_per_second"].mean())


def extract_orders_per_second_stat() -> None:
    log_reader = read_log_file_generator(f"{PATH}{LOG_FILE}")

    parsed_logs_df = convert_api_requests_to_dataframe(log_reader)
    parsed_logs_df.to_excel("orders.xlsx", index=False)

    show_orders_per_second_stat(parsed_logs_df)


if __name__ == "__main__":
    extract_orders_per_second_stat()
