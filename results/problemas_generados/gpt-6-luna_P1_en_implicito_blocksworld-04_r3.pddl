(define (problem blocks-problem)
  (:domain BLOCKS)
  (:objects
    a b c d - block
  )
  (:init
    (ontable a)
    (clear a)
    (ontable b)
    (clear b)
    (ontable c)
    (clear c)
    (ontable d)
    (clear d)
    (handempty)
  )
  (:goal (and
    (on d c)
    (on c b)
    (on b a)
  ))
)
