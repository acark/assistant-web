import { useRef, useState, useEffect, useCallback } from "react";
import Lottie from "lottie-react";
import { Box, Button } from "@mui/material";
import animationData from "../../assets/animations/robot.json";
import Vapi from "@vapi-ai/web";

const isPublicKeyMissingError = ({ vapiError }) => {
  return (
    !!vapiError &&
    vapiError.error.statusCode === 403 &&
    vapiError.error.error === "Forbidden"
  );
};

const assistantOptions = {
  name: "Vapi’s Pizza Front Desk",
  firstMessage: "Vappy’s Pizzeria speaking, how can I help you?",
  transcriber: {
    provider: "deepgram",
    model: "nova-2",
    language: "en-US",
  },
  voice: {
    provider: "playht",
    voiceId: "jennifer",
  },
  model: {
    provider: "openai",
    model: "gpt-4",
    messages: [
      {
        role: "system",
        content: `You are a voice assistant for Vappy’s Pizzeria, a pizza shop located on the Internet.
  
    Your job is to take the order of customers calling in. The menu has only 3 types
    of items: pizza, sides, and drinks. There are no other types of items on the menu.
  
    1) There are 3 kinds of pizza: cheese pizza, pepperoni pizza, and vegetarian pizza
    (often called "veggie" pizza).
    2) There are 3 kinds of sides: french fries, garlic bread, and chicken wings.
    3) There are 2 kinds of drinks: soda, and water. (if a customer asks for a
    brand name like "coca cola", just let them know that we only offer "soda")
  
    Customers can only order 1 of each item. If a customer tries to order more
    than 1 item within each category, politely inform them that only 1 item per
    category may be ordered.
  
    Customers must order 1 item from at least 1 category to have a complete order.
    They can order just a pizza, or just a side, or just a drink.
  
    Be sure to introduce the menu items, don't assume that the caller knows what
    is on the menu (most appropriate at the start of the conversation).
  
    If the customer goes off-topic or off-track and talks about anything but the
    process of ordering, politely steer the conversation back to collecting their order.
  
    Once you have all the information you need pertaining to their order, you can
    end the conversation. You can say something like "Awesome, we'll have that ready
    for you in 10-20 minutes." to naturally let the customer know the order has been
    fully communicated.
  
    It is important that you collect the order in an efficient manner (succinct replies
    & direct questions). You only have 1 task here, and it is to collect the customers
    order, then end the conversation.
  
    - Be sure to be kind of funny and witty!
    - Keep all your responses short and simple. Use casual language, phrases like "Umm...", "Well...", and "I mean" are preferred.
    - This is a voice conversation, so keep your responses short, like in a real conversation. Don't ramble for too long.`,
      },
    ],
  },
};

const vapi = new Vapi("b49b600b-2466-4a86-8ca9-116ad32194dc");

const CallPage = () => {
  const animationRef = useRef();
  const [isCalling, setIsCalling] = useState(false);
  const [connecting, setConnecting] = useState(false);
  const [connected, setConnected] = useState(false);

  const [assistantIsSpeaking, setAssistantIsSpeaking] = useState(false);
  const [volumeLevel, setVolumeLevel] = useState(0);

  const handleStartAnimation = () => {
    if (animationRef.current) {
      animationRef.current?.play?.();
    }
    setIsCalling(true);
  };

  const handleEndCall = () => {
    if (animationRef.current) {
      animationRef.current?.stop?.();
    }
    setIsCalling(false);
  };

  const startCallInline = async () => {
    const hasPermission = await checkMicrophonePermission();
    if (!hasPermission) return;
    if (isCalling) {
      handleEndCall();
      vapi.stop?.();
    } else {
      handleStartAnimation();
      setConnecting(true);
      vapi.start?.(assistantOptions);
    }
  };

  const checkMicrophonePermission = async () => {
    try {
      await navigator.mediaDevices.getUserMedia({ audio: true });
      return true;
    } catch (error) {
      console.error("Microphone access denied:", error);
      alert("Microphone access is required to start the call.");
      return false;
    }
  };

  // hook into Vapi events
  useEffect(() => {
    vapi.on("call-start", () => {
      setConnecting(false);
      setConnected(true);
    });

    vapi.on("call-end", () => {
      setConnecting(false);
      setConnected(false);
    });

    vapi.on("speech-start", () => {
      setAssistantIsSpeaking(true);
    });

    vapi.on("speech-end", () => {
      setAssistantIsSpeaking(false);
    });

    vapi.on("volume-level", (level) => {
      setVolumeLevel(level);
    });

    vapi.on("error", (error) => {
      console.error(error);

      setConnecting(false);
    });

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
        textAlign: "center",
      }}
    >
      <Lottie
        animationData={animationData}
        lottieRef={animationRef}
        loop={true}
        autoplay={false}
        style={{ width: 300, height: 300 }}
      />
      <Button
        variant="contained"
        color="primary"
        onClick={startCallInline}
        sx={{ mt: 4 }}
      >
        {isCalling ? "Aramayı Sonlandır" : "Arama Yap"}
      </Button>
    </Box>
  );
};

export default CallPage;
