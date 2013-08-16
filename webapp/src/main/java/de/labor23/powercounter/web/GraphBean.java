package de.labor23.powercounter.web;
import java.util.Date;
import java.util.List;

import javax.annotation.PostConstruct;
import javax.faces.bean.ManagedBean;
import javax.faces.bean.ViewScoped;

import org.primefaces.model.chart.CartesianChartModel;
import org.primefaces.model.chart.LineChartSeries;
import org.springframework.roo.addon.javabean.RooJavaBean;
import org.springframework.roo.addon.serializable.RooSerializable;

import de.labor23.powercounter.dm.PowerMeter;
import de.labor23.powercounter.dm.Tick;

@RooSerializable
@RooJavaBean
@ManagedBean
@ViewScoped
public class GraphBean {
	/**
	 * List of PowerMeters to calculate
	 */
	List<PowerMeter> powerMeters;
	
	/**
	 * Supposed time delta in miliseconds. Default=6000000 = 10 mins
	 */
	Integer timeDelta = 600000;
	
	/**
	 * Number of datapoints to display - currently fixed!
	 */
	Integer datapoints = 36;

	CartesianChartModel linearModel;
	
	
	@PostConstruct
    private void createLinearModel() {  
		powerMeters = PowerMeter.findAllPowerMeters();
        linearModel = new CartesianChartModel();  
        
        LineChartSeries lcs = null;
        Date now = new Date();
        Date from,to;
        Long countTicks;
        for( PowerMeter p : powerMeters ) {
            lcs = new LineChartSeries();  
            lcs.setLabel(p.getMeterName());
            
            //TODO: Calculate
            for(int i = 0; i<datapoints; i++) {
            	//get zeitraum in milis min/max
            	//search ticks between and powerMeter
            	from = new Date(now.getTime()-(timeDelta*(datapoints-i+1)));
            	to = new Date(now.getTime()-(timeDelta*(datapoints-i)));
            	countTicks = Tick.countTicksByOccurenceBetweenAndMeter(from, to, p);
            	
            	lcs.set(i, countTicks);
            }

        }
        linearModel.addSeries(lcs);  
    }  
}
