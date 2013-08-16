package de.labor23.powercounter.web.json;
import org.springframework.roo.addon.web.mvc.controller.json.RooWebJson;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

import de.labor23.powercounter.dm.json.TickDTO;

@RooWebJson(jsonObject = TickDTO.class)
@Controller
@RequestMapping("/ticks")
public class TickController {
}
