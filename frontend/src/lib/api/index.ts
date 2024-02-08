import axios from "axios";
import { BollingerBandSchema, CorrelationSchema, HeatmapSchema, StockPriceSchema } from "./schema";

type errorType = { message: string };
const baseURL = "http://127.0.0.1:5000"; // Replace 'your-api-port' with the actual port number

async function fetchData(endpoint: string, queryParams: { [key: string]: unknown } = {}) {
	try {
		const response = await axios.get(`${baseURL}/${endpoint}`, {
			params: queryParams
		});

		return response.data;
	} catch (error) {
		console.error("Error fetching data:", (error as errorType).message);
		throw error;
	}
}

export async function getCorrelationForHeatmap(stock_ticker: string) {
	try {
		const queryParams = {
			ticker: stock_ticker
		};

		const heatmapData = await fetchData("correlated_stocks", queryParams);
		return HeatmapSchema.parse(heatmapData);
	} catch (error) {
		console.error("Error fetching stock correlation data:", (error as errorType).message);
		throw error;
	}
}

/**
 * @param stock_ticker
 * @returns an array of tuples, where each tuple is of the form:
 * [date, open, high, low, close, adjClose, volume, symbol]
 */
export async function getStockPriceData(stock_ticker: string) {
	try {
		const queryParams = {
			ticker: stock_ticker
		};

		const stockPriceData = await fetchData("get_data", queryParams);
		return StockPriceSchema.parse(stockPriceData);
	} catch (error) {
		console.error("Error fetching stock price data:", (error as errorType).message);
		throw error;
	}
}

export async function getCorrelationBetweenStocks(
	stock_ticker1: string,
	stock_ticker2: string,
	start_date: string,
	end_date: string
) {
	try {
		// Define query parameters
		const queryParams = {
			stock1: stock_ticker1,
			stock2: stock_ticker2,
			sd: start_date,
			ed: end_date
		};

		const correlationData = await fetchData("correlation_info", queryParams);
		return CorrelationSchema.parse(correlationData);
	} catch (error) {
		console.error("Error fetching users data with params:", (error as errorType).message);
		throw error;
	}
}

export async function getBollingerBands(stock_ticker: string) {
	try {
		const queryParams = {
			stock1: stock_ticker,
			sd: "2019-11-10",
			ed: "2020-04-01",
			window: 20,
			num_std: 2
		};

		const bollingerBandsData = await fetchData("bollinger_bands", queryParams);
		return BollingerBandSchema.parse(bollingerBandsData);
	} catch (error) {
		console.error("Error fetching bollinger band data:", (error as errorType).message);
		throw error;
	}
}

// getStockPriceData("AAPL");
// getCorrelationForHeatmap("NVDA");
// getCorrelationBetweenStocks("GOOG", "BA", "2020-03-01", "2020-04-01");
