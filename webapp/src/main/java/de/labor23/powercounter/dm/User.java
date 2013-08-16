package de.labor23.powercounter.dm;
import java.util.ArrayList;
import java.util.List;

import javax.persistence.CascadeType;
import javax.persistence.Entity;
import javax.persistence.ManyToMany;

import org.springframework.beans.factory.annotation.Configurable;

import de.computerlyrik.spring.securityobjects.UserDetailsSO;

@Entity
@Configurable
public class User extends UserDetailsSO {

    /**
     */
    @ManyToMany(cascade = CascadeType.ALL, mappedBy = "user")
    private List<PowerMeter> powerMeters = new ArrayList<PowerMeter>();
}
