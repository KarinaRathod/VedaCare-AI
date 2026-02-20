// -----------------------------------------------------------
// 🌿🤖✨ EMOJI FORMATTER PACK v2000 — AI Ayurveda Assistant
// One file containing: keyword emojis + ayurveda emojis +
// emotional emojis + health emojis + random endings
// -----------------------------------------------------------

export function emojiFormatter(text) {
  const rules = [
    // 🌿 Ayurveda Concepts
    { key: /ayurveda/gi, emoji: "🌿" },
    { key: /dosha/gi, emoji: "⚖️" },
    { key: /vata/gi, emoji: "🌬️" },
    { key: /pitta/gi, emoji: "🔥" },
    { key: /kapha/gi, emoji: "💧" },

    // 💚 Health & Wellness
    { key: /health/gi, emoji: "💚" },
    { key: /wellness/gi, emoji: "🌱" },
    { key: /energy/gi, emoji: "⚡" },
    { key: /immunity|immune/gi, emoji: "🛡️" },
    { key: /protection/gi, emoji: "🛡️" },
    { key: /pain/gi, emoji: "💆‍♂️" },
    { key: /headache|migraine/gi, emoji: "🤕" },

    // 🧘 Mental Health
    { key: /stress/gi, emoji: "🧘‍♂️" },
    { key: /anxiety/gi, emoji: "😌" },
    { key: /calm/gi, emoji: "🌙" },
    { key: /sleep/gi, emoji: "😴" },

    // 🍃 Herbs & Remedies
    { key: /herb|herbal/gi, emoji: "🌱" },
    { key: /turmeric/gi, emoji: "🟡" },
    { key: /ashwagandha/gi, emoji: "🧪" },
    { key: /tulsi/gi, emoji: "🍃" },
    { key: /remedy|cure|treatment/gi, emoji: "🩺" },

    // 🍽️ Diet
    { key: /diet/gi, emoji: "🥗" },
    { key: /food/gi, emoji: "🍽️" },
    { key: /drink/gi, emoji: "🥤" },
    { key: /tea/gi, emoji: "🍵" },

    // ✨ Skin & Beauty
    { key: /skin/gi, emoji: "✨" },
    { key: /glow/gi, emoji: "🌟" },
    { key: /hair/gi, emoji: "💇‍♀️" },

    // ❤️ Emotional State
    { key: /happy/gi, emoji: "😊" },
    { key: /sad/gi, emoji: "😔" },

    // 🎯 Focus
    { key: /focus/gi, emoji: "🎯" },
    { key: /clarity/gi, emoji: "🔎" },

    // ✨ Boosting words
    { key: /improve/gi, emoji: "⬆️" },
    { key: /boost/gi, emoji: "🔋" },
    { key: /increase/gi, emoji: "📈" },
  ];

  let output = text;

  // Apply emoji replacements
  rules.forEach(rule => {
    output = output.replace(rule.key, match => `${match} ${rule.emoji}`);
  });

  return output;
}

// -----------------------------------------------------------
// Add random ending emojis for personality
// -----------------------------------------------------------

export function addEndingEmoji(text) {
  const endingPack = ["🌿", "💚", "✨", "😊", "🧘‍♂️", "🌱", "⚡", "🔥"];
  const random = endingPack[Math.floor(Math.random() * endingPack.length)];
  return `${text} ${random}`;
}

// -----------------------------------------------------------
// Final export: Full formatter
// -----------------------------------------------------------

export function formatWithEmojis(text) {
  return addEndingEmoji(emojiFormatter(text));
}
