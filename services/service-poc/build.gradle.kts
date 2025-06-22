plugins {
	java
	id("org.springframework.boot") version "3.5.3"
	id("io.spring.dependency-management") version "1.1.7"
}

group = "ua.ksa.poc"
version = "0.0.1-SNAPSHOT"

java {
	toolchain {
		version = JavaVersion.VERSION_21
	}
}

repositories {
	mavenCentral()
}

dependencies {
	implementation("org.springframework.boot:spring-boot-starter-webflux")
	implementation("org.springframework.integration:spring-integration-mqtt")
	implementation("org.eclipse.paho:org.eclipse.paho.client.mqttv3:1.2.5")
	testImplementation("org.springframework.boot:spring-boot-starter-test")
	testImplementation("io.projectreactor:reactor-test")
	testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}

tasks.withType<Test> {
	useJUnitPlatform()
}
