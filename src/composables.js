import { ref, watch } from 'vue';
import lqipData from '@/lqip-data.json';

/**
 * Composable for loading images with LQIP (Low Quality Image Placeholder)
 * @param {Ref} imageSrc - The full-quality image source
 * @param {Ref} imagePath - The original import path (from id field)
 * @returns {object} - { currentSrc, isLoading }
 */
export function useLQIP(imageSrc, imagePath = null) {
	const currentSrc = ref(null);
	const isLoading = ref(true);
	const aspectRatio = ref(null);

	const loadImage = (src, path) => {
		if (!src || typeof src !== 'string') {
			currentSrc.value = null;
			isLoading.value = false;
			return;
		}

		// Try to find LQIP data for this image
		const lqip = findLQIPData(src, path);
		
		if (lqip) {
			// Set placeholder first
			currentSrc.value = lqip.placeholder;
			aspectRatio.value = lqip.aspectRatio;
			isLoading.value = true;
		} else {
			// No LQIP data, just load the image directly
			currentSrc.value = src;
		}

		// Load full-quality image
		const img = new Image();
		img.onload = () => {
			currentSrc.value = src;
			isLoading.value = false;
		};
		img.onerror = () => {
			isLoading.value = false;
		};
		img.src = src;
	};

	// Watch for changes in image source and path
	if (imagePath) {
		watch([imageSrc, imagePath], ([newSrc, newPath]) => {
			loadImage(newSrc, newPath);
		}, { immediate: true });
	} else {
		watch(imageSrc, (newSrc) => {
			loadImage(newSrc, null);
		}, { immediate: true });
	}

	return {
		currentSrc,
		isLoading,
		aspectRatio,
	};
}

/**
 * Find LQIP data for a given image source
 */
function findLQIPData(src, originalPath) {
	if (!src || typeof src !== 'string') return null;

	// If we have the original path, use it directly for exact matching
	if (originalPath && typeof originalPath === 'string') {
		// Normalize path: @/assets/images -> src/assets/images
		const normalizedPath = originalPath.replace('@/', 'src/');
		
		if (lqipData[normalizedPath]) {
			return lqipData[normalizedPath];
		}
	}

	// Fallback: Try to match by path segments
	const srcSegments = src.split('/').filter(Boolean);
	const srcFilename = srcSegments[srcSegments.length - 1]?.split('-')[0] + '.avif';
	
	// Try to match by filename and path context
	for (const [path, data] of Object.entries(lqipData)) {
		const pathParts = path.split('/');
		const lqipFilename = pathParts[pathParts.length - 1];
		
		// Simple filename match
		if (lqipFilename === srcFilename) {
			return data;
		}
		
		// Try matching by last 2-3 segments of the path
		const lqipSegments = pathParts.slice(-3).join('/');
		if (src.includes(lqipSegments.replace(/\s+/g, '%20')) || 
		    src.includes(lqipSegments.replace(/\s+/g, '-'))) {
			return data;
		}
	}

	return null;
}
