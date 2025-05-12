import Swal, { SweetAlertIcon } from "sweetalert2";

export interface AlertOptions {
  title?: string;
  text?: string;
  icon?: SweetAlertIcon;
  confirmButtonText?: string;
  cancelButtonText?: string;
  timer?: number;
  showConfirmButton?: boolean;
  showCancelButton?: boolean;
  reverseButtons?: boolean;
  position?: "center" | "top" | "bottom" | "top-start" | "top-end" | "bottom-start" | "bottom-end";
}

export function showAlert(options: AlertOptions) {
  return Swal.fire({
    icon: options.icon || "info",
    title: options.title || "",
    text: options.text || "",
    confirmButtonText: options.confirmButtonText || "OK",
    cancelButtonText: options.cancelButtonText || "Cancelar",
    timer: options.timer,
    showConfirmButton: options.showConfirmButton,
    showCancelButton: options.showCancelButton,
    reverseButtons: options.reverseButtons,
    position: options.position,
  });
}
