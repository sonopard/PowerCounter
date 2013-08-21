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
		
		//amount of hours defined by timeframe
		Double hours = timeframe.doubleValue()/3600;
		
		countTicks = Tick.countTicksByOccurenceBetween(from.getTime(), to.getTime());
		Double ticksPerHour = countTicks/hours;
		
		//Uses an approx of 2000 ticks per hour emitted by PowerMeter
		Long watt = (long) (ticksPerHour*2000);
		
		return watt;
		
	}

}
