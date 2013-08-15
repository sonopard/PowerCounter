package de.labor23.powercounter.dm;
import org.springframework.roo.addon.javabean.RooJavaBean;
import org.springframework.roo.addon.jpa.activerecord.RooJpaActiveRecord;
import org.springframework.roo.addon.tostring.RooToString;
import javax.persistence.Column;
import javax.validation.constraints.Min;
import javax.validation.constraints.NotNull;

@RooJavaBean
@RooToString
@RooJpaActiveRecord(entityName = "PowerMeter", finders = { "findPowerMetersByGpioIdEquals" })
public class PowerMeter {

    /**
     */
    @NotNull
    @Column(unique = true)
    @Min(1L)
    private Integer gpioId;

    /**
     */
    private String meterName;
}
