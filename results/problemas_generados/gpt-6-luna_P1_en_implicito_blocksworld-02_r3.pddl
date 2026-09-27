(define (problem blocks-problem)
  (:domain BLOCKS)
  (:objects
    a b c d - block
  )
  (:init
    (ontable a)
    (clear a)
    (ontable b)
    (on c b)
    (clear c)
    (ontable d)
    (clear d)
    (handempty)
  )
  (:goal (and
    (on a b)
    (on b c)
    (on c d)
  ))
)
