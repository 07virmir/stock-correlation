<script lang="ts">
	import tbCorrelations from "$lib/data/correlations.json";
	import portfolioCorrelations from "$lib/data/portfolio-correlations.json";
	import { Moon } from "svelte-loading-spinners";
	import { fade } from "svelte/transition";
	import type { z } from "zod";
	import { tickerStore } from "../routes/top-bottom/+page.svelte";
	import StockPriceChart from "./StockPriceChart.svelte";
	import { getBollingerBands } from "./api";
	import type { BollingerBandSchema } from "./api/schema";

	export let tickers: [string, string];
	export let showModal: boolean;
	export let page: "top-bottom" | "portfolio";

	type bbt = z.infer<typeof BollingerBandSchema>;
	let bbData: [bbt, bbt];
	const options = { bb: true, sma: true };
	const colors = ["var(--accent)", "var(--accent-reverse)"];
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
	let statistics: [statObj, statObj];

	async function fetchData() {
		bbData = [await getBollingerBands(tickers[0]), await getBollingerBands(tickers[1])];
	}
	function fetchStatistics() {
		const correlations: any = page === "top-bottom" ? tbCorrelations : portfolioCorrelations;
		// @ts-ignore
		statistics = tickers.map(ticker => {
			let tickerData = correlations;
			if (page === "top-bottom") {
				tickerData = tickerData[$tickerStore];
			}
			tickerData = tickerData[ticker];
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
	}

	// Fetch data when the modal is opened
	$: if (showModal) {
		fetchData();
		fetchStatistics();
	}
</script>

<!-- svelte-ignore a11y-no-static-element-interactions -->
<div
	class="overlay"
	on:click={e => {
		if (e.target === e.currentTarget) {
			showModal = false;
		}
	}}
	on:keypress={e => {
		if (e.key === "Escape") {
			showModal = false;
		}
	}}
	transition:fade={{ duration: 100 }}
>
	<section>
		<div>
			<h1>{tickers[0]} vs {tickers[1]}</h1>
			{#if bbData}
				<StockPriceChart data={bbData} {tickers} {options} />
				<div class="options">
					<h3>Options:</h3>
					<div class="group">
						<input type="checkbox" id="bb" bind:checked={options.bb} />
						<label for="bb">Bollinger Bands</label>
					</div>
					<div class="group">
						<input type="checkbox" id="sma" bind:checked={options.sma} />
						<label for="sma">SMA</label>
					</div>
				</div>
				<table class="stats">
					<thead>
						<tr>
							<th></th>
							<th style={`color: ${colors[0]}`}>{tickers[0]}</th>
							<th style={`color: ${colors[1]}`}>{tickers[1]}</th>
						</tr>
					</thead>
					<tbody>
						{#each statTypes as stat}
							<tr>
								<td>{statNames[stat]}</td>
								<td>{statistics[0][stat].toFixed(5)}</td>
								<td>{statistics[1][stat].toFixed(5)}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			{:else}
				<Moon color="var(--accent)" size={50} />
			{/if}
		</div>
	</section>
</div>

<style lang="scss">
	.overlay {
		position: fixed;
		top: 0;
		left: 0;
		width: 100vw;
		height: 100vh;

		background-color: var(--overlay);
		backdrop-filter: blur(3px);

		section {
			position: absolute;
			top: 50%;
			left: 50%;
			transform: translate(-50%, -50%);
			width: 1200px;
			height: 1100px;
			border-radius: 10px;

			background-color: var(--bg);
			backdrop-filter: blur(10px);
			box-shadow: 0 0 10px 0 rgba(255, 255, 255, 0.05);
			@media (prefers-color-scheme: light) {
				border: none;
				box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.2);
			}

			& > div {
				display: flex;
				flex-direction: column;
				justify-content: center;
				align-items: center;
				width: 100%;
				height: 100%;

				h1 {
					font-size: 2.5rem;
					margin-bottom: 2rem;
				}

				.options {
					margin-top: 1rem;
					padding: 0.5rem;
					border-radius: 5px;
					border: 2px solid var(--text);
					display: flex;
					gap: 0.5rem;
					align-items: center;

					h3 {
						margin: 0;
					}

					.group {
						display: flex;
						align-items: center;
					}
				}
			}
		}
	}
</style>
