package ua.ksa.poc.mqtt;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Mono;

@RestController
public class CommandController {

    private final MqttConfig.MqttGateway mqttGateway;

    public CommandController(MqttConfig.MqttGateway mqttGateway) {
        this.mqttGateway = mqttGateway;
    }

    @PostMapping(path = "/api/command")
    public Mono<CommandResponse> command(@RequestBody CommandRequest command) {
        mqttGateway.sendToMqtt(command.command());
        return Mono.just(new CommandResponse(command.command()));
    }


    private record CommandRequest(String command) {
    }

    private record CommandResponse(String response) {
    }
}
