<script lang="ts" context="module">
	export const tickerStore = writable<keyof typeof correlationData>();
</script>

<script lang="ts">
	import Heatmap from "$lib/Heatmap.svelte";
	import TickerInput from "$lib/TickerInput.svelte";
	import correlationData from "$lib/data/correlations.json";
	import { writable } from "svelte/store";

	/* export let data;

	let transformedData = [
		...data.top_correlated_stocks
			.sort((a, b) => b[1] - a[1])
			.map(([ticker, value]) => ({
				x: ticker,
				y: data.ticker,
				value
			})),
		...data.bottom_correlated_stocks
			.sort((a, b) => b[1] - a[1])
			.map(([ticker, value]) => ({
				x: ticker,
				y: data.ticker,
				value
			}))
	]; */

	let newData: { x: string; y: string; value: number }[];

	function getTickerData() {
		if (!($tickerStore in correlationData)) {
			$tickerStore = "AAPL";
		}
		let tickerData = Object.entries(correlationData[$tickerStore]);
		tickerData = tickerData.slice(0, 1).concat(tickerData.slice(1).reverse());
		newData = [];
		for (const [ticker, data] of tickerData) {
			const correlations = Object.entries(data["correlations"]);
			for (const [correlatedTicker, correlation] of correlations) {
				newData.push({
					x: ticker,
					y: correlatedTicker,
					value: correlation as number
				});
			}
		}
	}
</script>

<h1>Top/Bottom Correlation Heatmap</h1>
<form on:submit={getTickerData}>
	<TickerInput bind:ticker={$tickerStore} />
	<button type="submit">Get Heatmap for Ticker</button>
</form>
{#if newData}
	<!-- <Heatmap data={transformedData} /> -->
	<Heatmap data={newData} page="top-bottom" />
{:else}
	<p>Enter a ticker to create a heatmap of its least and most correlated stocks!</p>
{/if}

<style lang="scss">
	h1 {
		text-align: center;
		font-size: 3rem;
		margin-bottom: 1rem;
	}

	form {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		gap: 0.5rem;
		margin-bottom: 1rem;
	}

	p {
		text-align: center;
		font-size: 1.25rem;
	}
</style>
