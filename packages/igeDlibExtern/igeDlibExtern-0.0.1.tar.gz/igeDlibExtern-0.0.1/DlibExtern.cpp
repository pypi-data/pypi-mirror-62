#include "DlibExtern.h"

DlibExtern::DlibExtern()
{
}

DlibExtern::~DlibExtern()
{
}

rectangle DlibExtern::detect(PyObject* image, int minWidth, int minHeight)
{
	static frontal_face_detector detector = get_frontal_face_detector();

	m_executor.wait_for_all();
	m_taskflow.clear();

	if (chosen_rect == nullptr)
	{
		chosen_rect = new rectangle();
	}

	auto _object = py::reinterpret_steal<py::object>(image);
	numpy_image<unsigned char> numpyImage = numpy_image<unsigned char>(_object);
	_object.release();

	m_taskflow.emplace(
		[this, numpyImage, minWidth, minHeight]() {

			std::vector<rectangle> faces;
			{
				faces = detector(numpyImage);
			}

			rectangle rect = rectangle(0, 0, 0, 0);
			for (std::vector<rectangle>::const_iterator it = faces.begin(); it != faces.end(); it++)
			{
				if (it->width() >= minWidth && it->height() >= minHeight && it->width() > rect.width() && it->height() > rect.height())
				{
					rect = rectangle(it->left(), it->right(), it->top(), it->bottom());
				}
			}
			chosen_rect->set_left(rect.left());
			chosen_rect->set_right(rect.right());
			chosen_rect->set_top(rect.top());
			chosen_rect->set_bottom(rect.bottom());
		}
	);

	m_executor.run(m_taskflow);
	return *chosen_rect;
}