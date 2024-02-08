<script lang="ts">
	import { page } from "$app/stores";
	import Flame from "./icons/Flame.svelte";
	import Heatmap from "./icons/Heatmap.svelte";
	import Stock from "./icons/Stock.svelte";
</script>

<nav>
	<div class="title">
		<Heatmap />
		<h1>Stock Correlation</h1>
	</div>
	<div class="links">
		<div class:active={$page.url.pathname.endsWith("top-bottom")}>
			<Flame />
			<a href="top-bottom"> Top/Bottom </a>
			<Flame />
		</div>
		<div class:active={$page.url.pathname.endsWith("portfolio")}>
			<Stock />
			<a href="portfolio"> Portfolio </a>
			<Stock />
		</div>
	</div>
</nav>

<style lang="scss">
	nav {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 2rem;

		margin: 0.5rem 0;

		.title {
			display: flex;
			flex-direction: row;
			align-items: center;
			gap: 0.5rem;
			font-size: 2.5rem;

			h1 {
				margin: 0;
				font-weight: 800;
				text-align: center;

				color: var(--accent);
			}
		}

		.links {
			display: flex;
			gap: 1.5rem;

			div {
				display: flex;
				flex-direction: row;
				align-items: center;
				font-size: 2rem;

				color: var(--text);

				a {
					display: inline-block;
					padding-inline: 0.25rem;

					color: inherit;
					border-radius: 0.5rem;
					font-weight: 600;

					transition: color 0.1s ease-in-out;
				}

				&:hover:not(.active) {
					color: var(--accent-light);
				}

				&.active {
					color: var(--accent);

					// Show an arrow below active link
					position: relative;
					&::after {
						content: "";
						position: absolute;
						bottom: -0.5rem;
						left: 50%;
						transform: translateX(-50%);
						width: 0;
						height: 0;
						border-left: 0.5rem solid transparent;
						border-right: 0.5rem solid transparent;
						border-bottom: 0.5rem solid var(--accent);
					}
				}
			}
		}
	}
</style>
