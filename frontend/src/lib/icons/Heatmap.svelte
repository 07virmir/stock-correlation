<script lang="ts">
	export let width: string = "2ex";
	export let height: string = "2ex";
</script>

<svg {width} {height} viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg">
  <g>
    <rect style="fill: rgb(255, 230, 230);" width="160" height="160" rx="10" ry="10"/>
    <rect style="fill: rgb(255, 198, 177);" width="160" height="160" rx="10" ry="10" x="170"/>
    <rect style="fill: rgb(255, 128, 82);" width="160" height="160" rx="10" ry="10" x="340"/>
    <rect style="fill: rgb(255, 198, 177);" width="160" height="160" rx="10" ry="10" y="170"/>
    <rect style="fill: rgb(255, 128, 82);" width="160" height="160" rx="10" ry="10" x="170" y="170"/>
    <rect style="fill: rgb(255, 88, 28);" width="160" height="160" rx="10" ry="10" x="340" y="170"/>
    <rect style="fill: rgb(255, 128, 82);" width="160" height="160" rx="10" ry="10" y="340"/>
    <rect style="fill: rgb(255, 88, 28);" width="160" height="160" rx="10" ry="10" x="170" y="340"/>
    <rect style="fill: rgb(255, 68, 0);" width="160" height="160" rx="10" ry="10" x="340" y="340"/>
  </g>
</svg>