<script lang="ts">
	import * as d3 from "d3";
	import { onMount } from "svelte";
	import HeatmapModal from "./HeatmapModal.svelte";
	import "./styles/Heatmap.scss";

	export let data: { x: string; y: string; value: number }[];
	export let page: "top-bottom" | "portfolio";
	export let width: number = 1000;
	export let height: number = 1000;

	function genHeatmap() {
		const margin = { top: 30, right: 0, bottom: 0, left: 60 };
		const innerWidth = width - margin.left - margin.right;
		const innerHeight = height - margin.top - margin.bottom;

		// If an svg already exists, remove it
		d3.select("#heatmap_vis").select("svg").remove();

		const svg = d3
			.select("#heatmap_vis")
			.append("svg")
			.attr("width", width)
			.attr("height", height)
			.append("g")
			.attr("transform", `translate(${margin.left},${margin.top})`);

		const x = d3
			.scaleBand()
			.range([0, innerWidth])
			.domain(data.map(d => d.x))
			.padding(0.05);
		svg.append("g").call(d3.axisTop(x).tickSize(0)).select(".domain").remove();

		const y = d3
			.scaleBand()
			.range([innerHeight, 0])
			.domain(data.map(d => d.y))
			.padding(0.05);
		svg.append("g").call(d3.axisLeft(y).tickSize(0)).select(".domain").remove();

		// @ts-ignore
		const colorScale = d3.scaleLinear().domain([-1, 0, 1]).range(["#0bf", "white", "#f40"]);

		svg.selectAll()
			.data(data, d => `${d!.x}:${d!.y}`)
			.enter()
			.append("rect")
			.attr("class", "heatmap-rect")
			.attr("x", d => x(d.x) ?? 0)
			.attr("y", d => y(d.y) ?? 0)
			.attr("rx", 5)
			.attr("ry", 5)
			.attr("width", x.bandwidth())
			.attr("height", y.bandwidth())
			.style("fill", d => colorScale(d.value))
			.on("click", pointerEvent => {
				const d = pointerEvent.target.__data__;
				modalTickers = [d.y, d.x];
				showModal = true;
			});

		svg.selectAll()
			.data(data)
			.enter()
			.append("text")
			.attr("class", "heatmap-text")
			// @ts-ignore
			.attr("x", d => x(d.x) + x.bandwidth() / 2)
			// @ts-ignore
			.attr("y", d => y(d.y) + y.bandwidth() / 2)
			.attr("dy", ".35em")
			.text(d => d.value.toFixed(2))
			.attr("text-anchor", "middle");
	}

	onMount(() => {
		genHeatmap();
	});

	$: {
		if (data) {
			genHeatmap();
		}
	}

	let showModal = false;
	let modalTickers: [string, string];
</script>

<div id="heatmap_vis"></div>
{#if showModal}
	<HeatmapModal bind:showModal tickers={modalTickers} {page} />
{/if}
