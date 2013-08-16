package de.labor23.powercounter.web;
import de.labor23.powercounter.dm.User;
import org.springframework.roo.addon.jsf.managedbean.RooJsfManagedBean;
import org.springframework.roo.addon.serializable.RooSerializable;

@RooSerializable
@RooJsfManagedBean(entity = User.class, beanName = "userBean")
public class UserBean {
}
