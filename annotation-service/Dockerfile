# Multistage Gradle Build
# based on:
# - https://stackoverflow.com/questions/25873971/docker-cache-gradle-dependencies
# - https://zwbetz.com/reuse-the-gradle-dependency-cache-with-docker/

FROM gradle:7-jdk11 AS build

##
# Step 1: Download Gradle Dependencies only
# (this will allow docker to cache them for later use)
##

RUN gradle --version && java -version

WORKDIR /home/gradle/src

# Only copy dependency-related files
COPY build.gradle settings.gradle gradlew /home/gradle/src/
COPY gradle /home/gradle/src/gradle/

# Only download dependencies
# Eat the expected build failure since no source code has been copied yet
RUN gradle clean build --no-daemon > /dev/null 2>&1 || true

##
# Step 2: Perform actual gradle build
##

# Copy all files
COPY --chown=gradle:gradle . .

# Do the actual build
# 'clean' will tell gradle to delete previous build artifacts
RUN gradle clean build --no-daemon --info

FROM eclipse-temurin:11

RUN mkdir /app

COPY --from=build /home/gradle/src/build/libs/annotation-service-0.0.1-SNAPSHOT.jar /app/spring-boot-application.jar

ENTRYPOINT ["java", "-XX:+UnlockExperimentalVMOptions", "-XX:+UseContainerSupport", "-jar", "/app/spring-boot-application.jar"]

EXPOSE 8083