package de.labor23.powercounter.dm;
import org.springframework.roo.addon.javabean.RooJavaBean;
import org.springframework.roo.addon.jpa.activerecord.RooJpaActiveRecord;
import org.springframework.roo.addon.tostring.RooToString;
import javax.persistence.Column;
import javax.validation.constraints.Min;
import javax.validation.constraints.NotNull;
import org.springframework.beans.factory.annotation.Value;

@RooJavaBean
@RooToString
@RooJpaActiveRecord(entityName = "PowerMeter", finders = { "findPowerMetersByGpioIdEquals", "findPowerMetersByAddress" })
public class PowerMeter {

    /**
     */
    private String meterName;

    /**
     */
    @NotNull
    private Byte address;

    /**
     */
    @NotNull
    @Value("2000")
    private Integer ticksPerKWH;
}
