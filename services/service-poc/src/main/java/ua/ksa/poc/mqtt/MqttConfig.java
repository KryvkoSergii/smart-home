package ua.ksa.poc.mqtt;

import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.integration.annotation.MessagingGateway;
import org.springframework.integration.annotation.ServiceActivator;
import org.springframework.integration.channel.DirectChannel;
import org.springframework.integration.core.MessageProducer;
import org.springframework.integration.mqtt.core.DefaultMqttPahoClientFactory;
import org.springframework.integration.mqtt.core.MqttPahoClientFactory;
import org.springframework.integration.mqtt.inbound.MqttPahoMessageDrivenChannelAdapter;
import org.springframework.integration.mqtt.outbound.MqttPahoMessageHandler;
import org.springframework.integration.mqtt.support.DefaultPahoMessageConverter;
import org.springframework.messaging.MessageChannel;
import org.springframework.messaging.MessageHandler;

@Configuration
public class MqttConfig {

    private final String mqttBrokerUrl = "tcp://localhost:1883";
    private final String clientId = "poc";
    private final String inputTopic = "fromDevice/topic" ;
    private final String outputTopic = "toDevice/topic" ;
//    private final String outputTopic = "output/topic";

    @Bean
    public MqttPahoClientFactory mqttClientFactory() {
        var factory = new DefaultMqttPahoClientFactory();
        var options = new MqttConnectOptions();
        options.setServerURIs(new String[]{mqttBrokerUrl});
        options.setCleanSession(true);
        factory.setConnectionOptions(options);
        return factory;
    }

    // Читання повідомлень
    @Bean
    public MessageProducer inbound() {
        MqttPahoMessageDrivenChannelAdapter adapter =
                new MqttPahoMessageDrivenChannelAdapter(clientId + "-in", mqttClientFactory(), inputTopic);
        adapter.setCompletionTimeout(5000);
        adapter.setConverter(new DefaultPahoMessageConverter());
        adapter.setQos(1);
        adapter.setOutputChannel(mqttInputChannel());
        return adapter;
    }

    @Bean
    public MessageChannel mqttInputChannel() {
        return new DirectChannel();
    }

    @Bean
    @ServiceActivator(inputChannel = "mqttInputChannel")
    public MessageHandler messageHandler() {
        return message -> {
            System.out.println("Received MQTT event: " + message.getPayload());
        };
    }

    // Відправлення повідомлень
    @Bean
    public MessageChannel mqttOutboundChannel() {
        return new DirectChannel();
    }

    @Bean
    @ServiceActivator(inputChannel = "mqttOutboundChannel")
    public MessageHandler mqttOutbound() {
        MqttPahoMessageHandler handler =
                new MqttPahoMessageHandler(clientId + "-out", mqttClientFactory());
        handler.setAsync(true);
        handler.setDefaultTopic(outputTopic);
        return handler;
    }

    // Gateway для публікації повідомлень
    @MessagingGateway(defaultRequestChannel = "mqttOutboundChannel")
    public interface MqttGateway {
        void sendToMqtt(String data);
    }
}