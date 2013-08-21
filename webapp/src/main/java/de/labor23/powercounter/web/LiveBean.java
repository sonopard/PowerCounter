package de.labor23.powercounter.web;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;

import javax.annotation.PostConstruct;
import javax.faces.bean.ManagedBean;
import javax.faces.bean.SessionScoped;

import org.primefaces.model.chart.MeterGaugeChartModel;
import org.springframework.roo.addon.javabean.RooJavaBean;
import org.springframework.roo.addon.serializable.RooSerializable;

import de.labor23.powercounter.dm.Tick;
import de.labor23.powercounter.web.util.WattageCalculatorUtil;

@RooSerializable
@RooJavaBean
@ManagedBean
@SessionScoped
public class LiveBean {
	
	List<Number> intervals;
	
	@PostConstruct
    private void createMeterGaugeModel() {  
    	  
        intervals = new ArrayList<Number>(){{  
            add(1000);  
            add(2000);  
            add(3000);  
            add(4000);  
            add(5000);  
            add(6000);  
        }};  
  
    }  
	
	public MeterGaugeChartModel getLoad() {
		
		Long watts = WattageCalculatorUtil.getCurrentWatts(3);
        return  new MeterGaugeChartModel(watts, intervals);  
	}
	
}
