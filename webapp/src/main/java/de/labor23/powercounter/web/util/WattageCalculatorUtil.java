package de.labor23.powercounter.web.util;

import java.util.Calendar;

import de.labor23.powercounter.dm.Tick;

public class WattageCalculatorUtil {
	
	/**
	 * returns average Watts used in timeframe seconds
	 * @param timeframe - in seconds
	 * @return
	 */
	public static Long getCurrentWatts(Integer timeframe) {
        Calendar from,to;
        Long countTicks;
		from = Calendar.getInstance();
		from.add(Calendar.SECOND, -timeframe);
		to = Calendar.getInstance();
		
		countTicks = Tick.countTicksByOccurenceBetween(from.getTime(), to.getTime());

		return calculateWatts(countTicks, timeframe);

		
	}
	
	public static Long calculateWatts(Long ticks, Integer timeframe) {
		//amount of hours defined by timeframe
		Double hours = timeframe.doubleValue()/3600;
		
		Double ticksPerHour = ticks/hours;
		
		//Uses an approx of 2000 ticks per kWh emitted by PowerMeter
		Long watts = (long) (ticksPerHour/2);
		
		return watts;
	}

}
