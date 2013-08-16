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
        Calendar from,to;
        Long countTicks;
		from = Calendar.getInstance();
		from.add(Calendar.SECOND, -10);
		to = Calendar.getInstance();
		
		countTicks = Tick.countTicksByOccurenceBetween(from.getTime(), to.getTime());
		
		Long watt = (countTicks*600/20);
		
        return  new MeterGaugeChartModel(watt, intervals);  
	}
	
}
