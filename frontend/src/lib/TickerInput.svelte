<script lang="ts">
	export let ticker: string;
</script>

<input
	type="text"
	bind:value={ticker}
	on:input={() => {
		ticker = ticker.toUpperCase().replace(/[^A-Z]/g, "");
	}}
	placeholder="Ticker"
/>

<style lang="scss">
	input {
		width: 8rem;
		height: 2rem;
		border-radius: 5px;
		border: none;
		background-color: var(--bg);
		color: var(--text);
		font-size: 1.25rem;
		font-family: inherit;
		text-align: center;
		box-shadow: 0 0 8px 0 #666;
		border: 2px solid white;

		@media (prefers-color-scheme: light) {
			border: 2px solid black;
		}

		&:focus {
			border-color: transparent;
			outline: 2px solid var(--accent);
		}
	}
</style>
