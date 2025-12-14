import { useState, useEffect } from "react";
import { FileUpload } from "@/components/ui/file-upload";
import { ExerciseDisplay } from "@/components/main/exerciseDisplay";
import { Button } from "@/components/ui/button";
import { BottomNav } from "../components/layout/bottomNav";
import { Card } from "@/components/ui/card";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Loader2, AlertCircle, CheckCircle, X } from "lucide-react";

export default function MainPage() {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<{
    type: "success" | "error" | null;
    message: string;
  }>({ type: null, message: "" });

  const API_BASE_URL = "/api";

  useEffect(() => {
    return () => {
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
    };
  }, [previewUrl]);

  const handleFileUpload = (files: File[]) => {
    if (files.length > 0) {
      const selectedFile = files[0];
      setFile(selectedFile);
      setUploadStatus({ type: null, message: "" });

      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
      const url = URL.createObjectURL(selectedFile);
      setPreviewUrl(url);

      console.log(selectedFile);
    }
  };

  const clearFile = () => {
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }
    setFile(null);
    setPreviewUrl(null);
    setUploadStatus({ type: null, message: "" });
  };

  const sendToBackend = async () => {
    if (!file) {
      setUploadStatus({
        type: "error",
        message: "Please select a file first",
      });
      return;
    }

    setIsUploading(true);
    setUploadStatus({ type: null, message: "" });

    try {
      const formData = new FormData();
      const fileType = file.type;
      const isVideo = fileType.startsWith("video/");
      const isImage = fileType.startsWith("image/");

      if (!isVideo && !isImage) {
        throw new Error("Please upload a valid video or image file");
      }

      const endpoint = isVideo
        ? `${API_BASE_URL}/arms/from_video`
        : `${API_BASE_URL}/arms/from_image`;

      if (isVideo) {
        formData.append("video", file);
        formData.append("fps", "1");
        formData.append("seconds", "-1");
      } else {
        formData.append("image", file);
      }

      const response = await fetch(endpoint, {
        method: "POST",
        body: formData,
      });

      let responseData = null;
      try {
        responseData = await response.json();
      } catch (jsonError) {
        console.error("Failed to parse JSON response:", jsonError);
      }

      if (!response.ok) {
        let errorMessage = `Server error (${response.status}): `;

        if (responseData) {
          const details = [];
          if (responseData.detail) details.push(responseData.detail);
          if (responseData.error) details.push(responseData.error);
          if (responseData.message) details.push(responseData.message);
          if (responseData.frame_index_in_valid_list !== undefined) {
            details.push(
              `Frame index: ${responseData.frame_index_in_valid_list}`
            );
          }

          errorMessage +=
            details.length > 0 ? details.join(" | ") : response.statusText;
        } else {
          errorMessage += response.statusText;
        }

        throw new Error(errorMessage);
      }

      setUploadStatus({
        type: "success",
        message: `${isVideo ? "Video" : "Image"} uploaded successfully!`,
      });

      console.log("Response:", responseData);
    } catch (error) {
      let errorMessage = "Failed to upload file";

      if (error instanceof TypeError && error.message === "Failed to fetch") {
        errorMessage =
          "Network error: Cannot connect to the server. Check if the API is running at " +
          API_BASE_URL;
      } else if (error instanceof Error) {
        errorMessage = error.message;
      }

      setUploadStatus({
        type: "error",
        message: errorMessage,
      });

      console.error("Upload error:", error);
    } finally {
      setIsUploading(false);
    }
  };

  const exerciseList = [
    { id: 1, name: "Push-ups", description: "Do 20 reps" },
    { id: 2, name: "Squats", description: "Do 15 reps" },
    { id: 3, name: "Plank", description: "Hold for 60s" },
    { id: 4, name: "Push-ups", description: "Do 20 reps" },
    { id: 5, name: "Squats", description: "Do 15 reps" },
  ];

  const isVideo = file?.type.startsWith("video/");

  return (
    <div className="w-full max-w-6xl mx-auto px-4 py-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div>
          <Card className="shadow-lg">
            <FileUpload onChange={handleFileUpload} />

            {file && previewUrl && (
              <div className="px-4 pb-4">
                <div className="relative mb-4 bg-gray-100 rounded-lg overflow-hidden">
                  <button
                    onClick={clearFile}
                    className="absolute top-2 right-2 z-10 bg-red-500 text-white rounded-full p-1 hover:bg-red-600 transition-colors"
                    aria-label="Clear file"
                  >
                    <X className="h-4 w-4" />
                  </button>

                  {isVideo ? (
                    <video
                      src={previewUrl}
                      controls
                      className="w-full max-h-96 object-contain"
                    >
                      Your browser does not support video preview.
                    </video>
                  ) : (
                    <img
                      src={previewUrl}
                      alt="Preview"
                      className="w-full max-h-96 object-contain"
                    />
                  )}
                </div>

                <p className="text-sm text-gray-600 mb-3">
                  <span className="font-semibold">File:</span> {file.name}
                  <br />
                  <span className="font-semibold">Size:</span>{" "}
                  {(file.size / 1024 / 1024).toFixed(2)} MB
                  <br />
                  <span className="font-semibold">Type:</span>{" "}
                  {isVideo ? "Video" : "Image"}
                </p>

                <Button
                  variant="default"
                  size="lg"
                  className="text-white w-full mb-2"
                  onClick={sendToBackend}
                  disabled={isUploading}
                >
                  {isUploading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Uploading...
                    </>
                  ) : (
                    "Send to API"
                  )}
                </Button>
              </div>
            )}

            {uploadStatus.type && (
              <div className="px-4 pb-4">
                <Alert
                  variant={
                    uploadStatus.type === "error" ? "destructive" : "default"
                  }
                  className={
                    uploadStatus.type === "success"
                      ? "border-green-500 bg-green-50"
                      : ""
                  }
                >
                  {uploadStatus.type === "error" ? (
                    <AlertCircle className="h-4 w-4" />
                  ) : (
                    <CheckCircle className="h-4 w-4 text-green-600" />
                  )}
                  <AlertTitle>
                    {uploadStatus.type === "error" ? "Error" : "Success"}
                  </AlertTitle>
                  <AlertDescription className="break-words">
                    {uploadStatus.message}
                  </AlertDescription>
                </Alert>
              </div>
            )}

            <div className="px-4 pb-4"></div>
          </Card>
        </div>
        <div>
          <ExerciseDisplay exercises={exerciseList} />
        </div>
      </div>

      <BottomNav />
    </div>
  );
}
