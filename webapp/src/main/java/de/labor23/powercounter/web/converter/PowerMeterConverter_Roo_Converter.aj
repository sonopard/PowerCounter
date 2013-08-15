// WARNING: DO NOT EDIT THIS FILE. THIS FILE IS MANAGED BY SPRING ROO.
// You may push code into the target .java compilation unit if you wish to edit any member(s).

package de.labor23.powercounter.web.converter;

import de.labor23.powercounter.dm.PowerMeter;
import de.labor23.powercounter.web.converter.PowerMeterConverter;
import javax.faces.component.UIComponent;
import javax.faces.context.FacesContext;
import javax.faces.convert.Converter;
import javax.faces.convert.FacesConverter;

privileged aspect PowerMeterConverter_Roo_Converter {
    
    declare parents: PowerMeterConverter implements Converter;
    
    declare @type: PowerMeterConverter: @FacesConverter("de.labor23.powercounter.web.converter.PowerMeterConverter");
    
    public Object PowerMeterConverter.getAsObject(FacesContext context, UIComponent component, String value) {
        if (value == null || value.length() == 0) {
            return null;
        }
        Long id = Long.parseLong(value);
        return PowerMeter.findPowerMeter(id);
    }
    
    public String PowerMeterConverter.getAsString(FacesContext context, UIComponent component, Object value) {
        return value instanceof PowerMeter ? ((PowerMeter) value).getId().toString() : "";
    }
    
}