const input = document.querySelector('#phone');
let intlTelInput;

const countryMap = {
    ru: "912 345-67-89",
    ua: "50 123 4567",
    kz: "771 000 9998",
    by: "29 491-19-11",
    md: "37360249945",
    us: "1 202-657-0144",
    custom: "1 202-555-0135"
};

document.addEventListener('DOMContentLoaded', () => {
    window.intlTelInputGlobals.getCountryData().push({
        name: "your country",
        iso2: "custom",
        dialCode: "",
        priority: 0,
        areaCodes: null
    });
    intlTelInput = window.intlTelInput(input, {
        onlyCountries: ['ru', 'ua', 'kz', 'by','md','us', 'custom'],
        initialCountry: 'md',
        separateDialCode: true,
    });
});

input.addEventListener("countrychange", () => {
    input.placeholder = countryMap[intlTelInput.getSelectedCountryData().iso2];
});

document.querySelector("#main-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    document.querySelector('main').style.cssText = "animation:blur; animation-duration:0.6s; animation-fill-mode:both";
    document.querySelector('footer').style.cssText = document.querySelector('main').style.cssText;

    setTimeout(() => document.querySelector('#block-ui').style.display = "block", 600);

    const formData = new FormData(document.querySelector('#main-form'));
    formData.append('phone_code', intlTelInput.getSelectedCountryData().dialCode);

    const response = await fetch("/attack/start", {
        method: 'POST',
        body: formData,
    });
    if (response) {
        document.querySelector('main').style.cssText = "animation:blur; animation-duration:0.6s; animation-fill-mode:both; animation-direction:reverse";
        document.querySelector('footer').style.cssText = document.querySelector('main').style.cssText;
        
        setTimeout(() => document.querySelector('#block-ui').style.display = "none", 600);
    }
});
