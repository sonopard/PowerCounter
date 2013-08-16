package de.labor23.powercounter.web;
import java.util.Calendar;
import java.util.Date;

import javax.annotation.PostConstruct;
import javax.faces.bean.ManagedBean;
import javax.faces.bean.SessionScoped;

import org.primefaces.model.chart.CartesianChartModel;
import org.primefaces.model.chart.LineChartSeries;
import org.springframework.roo.addon.javabean.RooJavaBean;
import org.springframework.roo.addon.serializable.RooSerializable;

import de.labor23.powercounter.dm.PowerMeter;
import de.labor23.powercounter.dm.Tick;
import de.labor23.powercounter.dm.User;

@RooSerializable
@RooJavaBean
@ManagedBean
@SessionScoped
public class ShowUserBean {
	
	private User user;
	
	public CartesianChartModel getLastDays(Integer days) {
        CartesianChartModel linearModel = new CartesianChartModel(); 
        Calendar now = Calendar.getInstance();
        Calendar from,to;
        LineChartSeries lcs;
        Long countTicks;
        for( PowerMeter p : user.getPowerMeters() ) {
            lcs = new LineChartSeries();  
            lcs.setLabel(p.getMeterName());
            for(int i = 0; i>-days; i--) {
            	//get zeitraum in milis min/max
            	//search ticks between and powerMeter
            	from = Calendar.getInstance();
            	from.add(Calendar.MONTH, i-1);
            	to = Calendar.getInstance();
            	to.add(Calendar.MONTH, i);
            	countTicks = Tick.countTicksByOccurenceBetweenAndMeter(from.getTime(), to.getTime(), p);
            	
            	lcs.set(i, countTicks);
            }
            linearModel.addSeries(lcs);  
        }
        return linearModel;
	}
	
}
