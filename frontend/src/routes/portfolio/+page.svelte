<script lang="ts">
	import Heatmap from "$lib/Heatmap.svelte";
	import TickerInput from "$lib/TickerInput.svelte";
	import correlationData from "$lib/data/portfolio-correlations.json";

	// @ts-ignore
	const tickers: (keyof typeof correlationData)[] = Array.from({ length: 5 }, () => "");
	let heatmapData: { x: string; y: string; value: number }[];
	let tickerSet = new Set<(typeof tickers)[number]>();

	const statTypes = ["cumret", "adr", "sddr", "jenson", "info", "treynor"] as const;
	const statNames: Record<(typeof statTypes)[number], string> = {
		cumret: "Cumulative Returns",
		adr: "Avg Daily Return",
		sddr: "Std Dev of Daily Returns",
		jenson: "Jenson's Alpha",
		info: "Information Ratio",
		treynor: "Treynor Ratio"
	};
	type statObj = Record<(typeof statTypes)[number], number>;
	let statistics: statObj[];
	let portStats: statObj;
	function getHeatmapData() {
		heatmapData = [];
		tickerSet = new Set();
		for (let i = 0; i < tickers.length; i++) {
			const ticker = tickers[i];
			if (!(ticker in correlationData)) {
				continue;
			}
			tickerSet.add(ticker);
			const tickerData = correlationData[ticker]["correlations"];
			for (let j = i + 1; j < tickers.length + i + 1; j++) {
				const correlatedTicker = tickers[j % tickers.length];
				if (!(correlatedTicker in tickerData)) {
					continue;
				}
				// @ts-ignore
				const correlation = tickerData[correlatedTicker];
				heatmapData.push({
					x: ticker,
					y: correlatedTicker,
					value: correlation as number
				});
			}
		}

		heatmapData = heatmapData
			.slice(0, tickerSet.size - 1)
			.toReversed()
			.concat(heatmapData.slice(tickerSet.size - 1));
	}
	function getStatistics() {
		statistics = [...tickerSet].map(ticker => {
			const tickerData = correlationData[ticker];
			const portMets = tickerData["portfolio_metrics"];
			return {
				cumret: portMets["cum_return"],
				adr: portMets["avg_daily_return"],
				sddr: portMets["std_daily_return"],
				jenson: tickerData["jensen_alpha"],
				info: tickerData["information_ratio"],
				treynor: tickerData["treynor_ratio"]
			};
		});
		console.log(statistics);
		// @ts-ignore
		portStats = {};
		for (const statType of statTypes) {
			let sum = 0;
			for (const stat of statistics) {
				sum += stat[statType];
			}
			portStats[statType] = sum / statistics.length;
		}
		console.log(statistics, portStats);
	}
	function getData() {
		getHeatmapData();
		getStatistics();
	}
</script>

<h1>Portfolio</h1>

<h2>Tickers</h2>
<form class="tickers" on:submit={getData}>
	<div>
		{#each tickers as ticker, i}
			<TickerInput bind:ticker />
		{/each}
	</div>
	<button type="submit">Get Heatmap for Tickers</button>
</form>

{#if heatmapData}
	<Heatmap
		data={heatmapData}
		page="portfolio"
		width={150 * tickerSet.size + 30}
		height={150 * tickerSet.size}
	/>
	<div class="stats-wrapper">
		<table class="stats">
			<thead>
				<tr>
					<th></th>
					<th>Portfolio Stats</th>
				</tr>
			</thead>
			<tbody>
				{#each statTypes as stat}
					<tr>
						<td>{statNames[stat]}</td>
						<td>{portStats[stat].toFixed(5)}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
{:else}
	<p>Enter tickers to create a heatmap and get statistics!</p>
{/if}

<style lang="scss">
	h1 {
		text-align: center;
		font-size: 3rem;
	}

	h2 {
		text-align: center;
		font-size: 2rem;
		margin-bottom: 1rem;
	}

	.tickers {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		gap: 1rem;

		div {
			display: flex;
			justify-content: center;
			align-items: center;
			gap: 1rem;
			text-align: center;
		}
	}

	p {
		text-align: center;
		font-size: 1.5rem;
	}

	.stats-wrapper {
		display: flex;
		justify-content: center;
	}
</style>
