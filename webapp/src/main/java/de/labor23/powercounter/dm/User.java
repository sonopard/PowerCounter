package de.labor23.powercounter.dm;
import org.springframework.roo.addon.javabean.RooJavaBean;
import org.springframework.roo.addon.jpa.activerecord.RooJpaActiveRecord;
import org.springframework.roo.addon.jpa.entity.RooJpaEntity;
import org.springframework.roo.addon.tostring.RooToString;

import de.computerlyrik.spring.securityobjects.UserDetailsSO;

import java.util.ArrayList;
import java.util.List;

import javax.persistence.CascadeType;
import javax.persistence.ManyToMany;

@RooJavaBean
@RooToString
public class User extends UserDetailsSO {

    /**
     */
    @ManyToMany(cascade = CascadeType.ALL)
    private List<PowerMeter> powerMeters = new ArrayList<PowerMeter>();
}
