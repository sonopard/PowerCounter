package de.labor23.powercounter.web;
import de.labor23.powercounter.dm.PowerMeter;
import org.springframework.roo.addon.jsf.managedbean.RooJsfManagedBean;
import org.springframework.roo.addon.serializable.RooSerializable;

@RooSerializable
@RooJsfManagedBean(entity = PowerMeter.class, beanName = "powerMeterBean")
public class PowerMeterBean {
}
