package de.labor23.powercounter.web.json;
import de.labor23.powercounter.dm.Tick;
import org.springframework.roo.addon.web.mvc.controller.json.RooWebJson;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

@RooWebJson(jsonObject = Tick.class)
@Controller
@RequestMapping("/ticks")
public class TickController {
}
