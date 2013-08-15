package de.labor23.powercounter.web;
import de.labor23.powercounter.dm.Tick;
import org.springframework.roo.addon.jsf.managedbean.RooJsfManagedBean;
import org.springframework.roo.addon.serializable.RooSerializable;

@RooSerializable
@RooJsfManagedBean(entity = Tick.class, beanName = "tickBean")
public class TickBean {
}
