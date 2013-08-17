package de.labor23.powercounter.web;
import java.util.List;

import javax.annotation.PostConstruct;
import javax.faces.bean.ManagedBean;
import javax.faces.bean.ManagedProperty;
import javax.faces.bean.ViewScoped;

import org.primefaces.event.DragDropEvent;
import org.springframework.roo.addon.javabean.RooJavaBean;
import org.springframework.roo.addon.serializable.RooSerializable;

import de.labor23.powercounter.dm.PowerMeter;
import de.labor23.powercounter.dm.User;

@RooSerializable
@RooJavaBean
@ManagedBean
@ViewScoped
public class UserBean {
	
	private User user;
	private List<User> allUsers;
	
	@PostConstruct
	private void setUp() {
		allUsers = User.findAllUsers();
		/* For testing purpose only */
		user = (User) User.findAllUserDetailsSO().get(0);
	}


    @ManagedProperty(value = "#{powerMeterBean.unusedPowerMeters}")
	public List<PowerMeter> unusedPowerMeters;    
    
    public List<PowerMeter> getUserPowerMeters() {
    	return PowerMeter.findPowerMetersByUser(user).getResultList();
    }
    
    public void onPowerMeterDropIn(DragDropEvent ddEvent) {  
        PowerMeter meter  = ((PowerMeter) ddEvent.getData());  
        unusedPowerMeters.remove(meter);
        meter.setUser(user);
        meter.merge();
    }  
    
    public void onPowerMeterDropOut(DragDropEvent ddEvent) {  
        PowerMeter meter  = ((PowerMeter) ddEvent.getData());  
        unusedPowerMeters.add(meter);
        meter.setUser(null);
        meter.merge();
    }
	
}
