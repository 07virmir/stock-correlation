import { z } from "zod";

const HeatmapStockSchema = z.tuple([z.string(), z.coerce.number()]);
export const HeatmapSchema = z.object({
	bottom_correlated_stocks: z.array(HeatmapStockSchema),
	ticker: z.string(),
	top_correlated_stocks: z.array(HeatmapStockSchema)
});

const SingleStockPriceSchema = z.tuple([
	z.coerce.date(), // date
	z.number(), // open
	z.number(), // high
	z.number(), // low
	z.number(), // close
	z.number(), // adjClose
	z.number(), // volume
	z.string() // symbol
]);
export const StockPriceSchema = z.array(SingleStockPriceSchema);

export const CorrelationSchema = z.object({
	correlation: z.number()
});

const bbDataPointSchema = z.record(z.string(), z.number());
export const BollingerBandSchema = z.object({
	"%B": bbDataPointSchema,
	Lower_Band: bbDataPointSchema,
	Overbought: bbDataPointSchema,
	Oversold: bbDataPointSchema,
	SMA: bbDataPointSchema,
	STD: bbDataPointSchema,
	Stock_Price: bbDataPointSchema,
	Upper_Band: bbDataPointSchema
});
