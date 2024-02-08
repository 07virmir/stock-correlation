import { getCorrelationForHeatmap } from "$lib/api";

export async function load() {
	const data = await getCorrelationForHeatmap("AAPL");
	return data;
}
