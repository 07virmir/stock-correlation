<script lang="ts">
	import * as d3 from "d3";
	import { onMount } from "svelte";
	import type { z } from "zod";
	import type { BollingerBandSchema } from "./api/schema";
	import "./styles/StockPrice.scss";

	type bbt = z.infer<typeof BollingerBandSchema>;
	export let data: [bbt, bbt];
	export let tickers: [string, string];
	export let options: { bb: boolean; sma: boolean };
	export let width: number = 1100;
	export let height: number = 500;

	const margin = { top: 5, right: 0, bottom: 50, left: 60 };
	const innerWidth = width - margin.left - margin.right;
	const innerHeight = height - margin.top - margin.bottom;

	const firstStock = data[0];
	const lineColors: [string, string] = ["var(--accent)", "var(--accent-reverse)"];
	const areaColors: [string, string] = ["var(--accent-light)", "var(--accent-reverse-light)"];

	let tooltip: d3.Selection<HTMLDivElement, unknown, HTMLElement, any>;
	let markers: d3.Selection<SVGCircleElement, unknown, HTMLElement, any>[];
	let smaMarkers: d3.Selection<SVGCircleElement, unknown, HTMLElement, any>[];

	function genChart() {
		// If an svg already exists, remove its contents
		d3.select("#stock-price-chart").selectChildren().remove();
		// If a tooltip already exists, remove it
		d3.select(".stock-price-tooltip").remove();

		const svg = d3.select("#stock-price-chart").attr("width", width).attr("height", height);

		const g = svg.append("g").attr("transform", `translate(${margin.left},${margin.top})`);

		// Define the scales
		const xScale = d3
			.scaleTime()
			.domain([
				new Date(Object.keys(firstStock.Stock_Price)[0]),
				new Date(Object.keys(firstStock.Stock_Price).at(-1) as string)
			]) // input: dates
			.range([0, innerWidth]); // output: pixels
		const yScale = d3
			.scaleLinear()
			.domain([0, Math.max(...data.flatMap(stock => Object.values(stock["Upper_Band"])))]) // input: closing prices
			.range([innerHeight, 0]); // output: pixels

		// Create lines group
		const lines = g.append("g").attr("class", "lines");

		// Create the legend
		const legendPadding = { x: 10, y: 10 };
		const legend = svg
			.append("g")
			.attr("class", "legend")
			.attr(
				"transform",
				`translate(${width - margin.right - legendPadding.x}, ${
					margin.top + legendPadding.y
				})`
			);

		const lineGenerator = d3
			.line<[string, number]>()
			.x(d => xScale(new Date(d[0])))
			.y(d => yScale(d[1]));

		const areaGenerator = d3
			.area<[string, number, number]>()
			.x(d => xScale(new Date(d[0])))
			.y0(d => yScale(d[1]))
			.y1(d => yScale(d[2]));

		// Create the lines
		data.forEach((stock, i) => {
			lines
				.append("path")
				.attr("class", "line")
				.datum(Object.entries(stock.Stock_Price))
				.attr("fill", "none")
				.attr("stroke", lineColors[i])
				.attr("stroke-width", 1.5)
				.attr("d", lineGenerator);

			if (options.sma) {
				lines
					.append("path")
					.attr("class", "line")
					.datum(Object.entries(stock.SMA))
					.attr("fill", "none")
					.attr("stroke", areaColors[i])
					.attr("stroke-width", 1.5)
					.attr("d", lineGenerator);
			}

			if (options.bb) {
				lines
					.append("path")
					.attr("class", "line upper-band")
					.datum(Object.entries(stock.Upper_Band))
					.attr("fill", "none")
					.attr("stroke", lineColors[i])
					.attr("stroke-width", 1)
					.attr("stroke-dasharray", "5,5")
					.attr("d", lineGenerator);

				lines
					.append("path")
					.attr("class", "line lower-band")
					.datum(Object.entries(stock.Lower_Band))
					.attr("fill", "none")
					.attr("stroke", lineColors[i])
					.attr("stroke-width", 1)
					.attr("stroke-dasharray", "5,5")
					.attr("d", lineGenerator);

				lines
					.append("path")
					.attr("class", "area")
					.datum(
						Object.entries(stock.Upper_Band).map(([date, upperValue]) => {
							const lowerValue = stock.Lower_Band[date];
							return [date, upperValue, lowerValue];
						})
					)
					.attr("fill", areaColors[i])
					.attr("opacity", 0.2)
					// @ts-ignore
					.attr("d", areaGenerator);
			}

			const legendRow = legend.append("g").attr("transform", `translate(0, ${i * 20})`);

			legendRow
				.append("rect")
				.attr("width", 10)
				.attr("height", 10)
				.attr("fill", lineColors[i]);

			legendRow
				.append("text")
				.attr("x", -10)
				.attr("y", 10)
				.attr("text-anchor", "end")
				.style("text-transform", "capitalize")
				.style("fill", "var(--text)")
				.text(tickers[i]); // assuming the ticker symbol is at index 7
		});

		// Create the x axis
		const xAxis = g
			.append("g")
			.attr("class", "x-axis")
			.attr("transform", `translate(0,${innerHeight})`)
			.call(d3.axisBottom(xScale));

		xAxis
			.append("text")
			.attr("class", "axis-label x-label")
			.attr("x", innerWidth / 2)
			.attr("y", margin.bottom)
			.attr("text-anchor", "middle")
			.text("Date");

		// Create the y axis
		const yAxis = g.append("g").attr("class", "y-axis").call(d3.axisLeft(yScale));

		yAxis
			.append("text")
			.attr("class", "axis-label y-label")
			.attr("transform", "rotate(-90)")
			.attr("x", -innerHeight / 2)
			.attr("y", -margin.left)
			.attr("text-anchor", "middle")
			// Adjust vertical text anchor to top
			.attr("dominant-baseline", "hanging")
			.text("Closing Price");

		// Create the tooltip
		tooltip = d3
			.select("body")
			.append("div")
			.attr("class", "stock-price-tooltip")
			.style("display", "none");

		// Create the markers
		markers = data.map(() => svg.append("circle").attr("r", 5).style("display", "none"));
		if (options.sma) {
			smaMarkers = data.map(() => svg.append("circle").attr("r", 5).style("display", "none"));
		}

		svg.on("mousemove", event => {
			const [x, y] = d3.pointer(event);
			// Convert to date string to remove time from Date object
			const date = new Date(xScale.invert(x - margin.left).toDateString());

			// Find the data point closest to the mouse position
			const prices = data.map((stock, i) => {
				const closestValueIndex = d3.bisectLeft(
					Object.keys(stock.Stock_Price),
					date.toISOString().slice(0, 10)
				);
				const closestDate = Object.keys(stock.Stock_Price)[closestValueIndex];
				const stockPrice = stock.Stock_Price[closestDate];
				const smaPrice = stock.SMA[closestDate];

				markers[i]
					.attr("cx", xScale(new Date(closestDate)) + margin.left)
					.attr("cy", yScale(stockPrice) + margin.top)
					.attr("fill", lineColors[i])
					.style("display", "block");

				if (options.sma) {
					smaMarkers[i]
						.attr("cx", xScale(new Date(closestDate)) + margin.left)
						.attr("cy", yScale(smaPrice) + margin.top)
						.attr("fill", areaColors[i])
						.style("display", "block");
				}

				return [stockPrice.toFixed(2), smaPrice.toFixed(2)];
			});

			const dateFormatter = d3.timeFormat("%b %d, %Y");
			const formattedDate = dateFormatter(date);

			tooltip
				.style("left", `${event.pageX + 10}px`)
				.style("top", `${event.pageY + 10}px`)
				.style("display", "block")
				.html(
					`${formattedDate}<br/>` +
						prices
							.map(
								(price, i) =>
									`<b style="color: ${lineColors[i]}">${tickers[i]}:</b> $${
										price[0]
									} ${
										options.bb || options.sma
											? `(<span style="color: ${areaColors[i]}">${price[1]}</span>)`
											: ""
									}`
							)
							.join("<br>")
				);
		});

		svg.on("mouseleave", () => {
			markers.forEach(marker => marker.style("display", "none"));
			if (options.sma) smaMarkers.forEach(marker => marker.style("display", "none"));
			tooltip.style("display", "none");
		});
	}

	onMount(() => {
		genChart();
	});

	$: if (options) {
		genChart();
	}
</script>

<svg id="stock-price-chart" />
